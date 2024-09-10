from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.signals import user_logged_in
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from foundation.helpers import log_error
from foundation.serializers.auth import LoginSerializer, RegisterUserSerializer
from foundation.serializers.shared import ErrRespSerializer, ValidationErrSerializer
from foundation.serializers.user import UserSerializer, UserWithTokenSerializer


class RegisterUserAPIView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=RegisterUserSerializer,
        responses={
            201: UserWithTokenSerializer,
            400: ValidationErrSerializer,
            409: ErrRespSerializer,
            500: ErrRespSerializer,
        },
    )
    def post(self, request):
        try:
            serializer = RegisterUserSerializer(data=request.data)
            if not serializer.is_valid():
                validation_errors = {field: errors[0] for field, errors in serializer.errors.items()}
                return Response(
                    ValidationErrSerializer({"errors": validation_errors}).data,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            email = serializer.validated_data["email"].lower()
            validated_data = {**serializer.validated_data, "email": email}

            if get_user_model().objects.filter(email=email).exists():
                return Response(
                    ErrRespSerializer({"message": "A user with that email already exists!"}).data,
                    status=status.HTTP_409_CONFLICT,
                )

            user = get_user_model().objects.create_user(**validated_data)
            access_token = RefreshToken.for_user(user).access_token

            user_logged_in.send(sender=user.__class__, request=request, user=user)
            return Response(
                UserWithTokenSerializer({"access_token": str(access_token), "user": user}).data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as ex:
            log_error("ERROR occurred in RegistrationAPIView", ex)
            return Response(
                ErrRespSerializer(
                    {"message": "Some error occurred. Please contact administrator."}
                ).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            email = serializer.validated_data["email"].lower()
            validated_data = {**serializer.validated_data, "email": email}

            user = authenticate(request, **validated_data)
            if not user:
                return Response(
                    {"message": "Email and password do not match."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            access_token = RefreshToken.for_user(user).access_token
            user_logged_in.send(sender=user.__class__, request=request, user=user)
            return Response(
                {
                    "access_token": str(access_token),
                    "data": UserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )

        except exceptions.PermissionDenied as ex:
            return Response({"message": str(ex)}, status=status.HTTP_403_FORBIDDEN)

        except Exception as ex:
            log_error("ERROR occurred in LoginAPIView", ex)
            return Response(
                {"message": "Some error occurred. Please contact administrator."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoggedInUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = UserSerializer(request.user).data
            return Response(dict(data=data))

        except Exception as e:
            log_error(f"Error occurred in LoggedInUserAPIView GET", e)

            return Response(
                {"message": "Some error occurred. Please contact administrator."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
