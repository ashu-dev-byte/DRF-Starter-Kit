"""
URL configuration for drf_starter_kit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from foundation import views


# Auth Routes
auth_url_patterns = [
    path(
        r"register-user",
        views.RegisterUserAPIView.as_view(),
        name="api.register-user",
    ),
    path(r"login", views.LoginAPIView.as_view(), name="api.login"),
]

# Api Routes
api_url_patterns = [
    re_path("auth/", include(auth_url_patterns)),
    ##### User Routes
    path("me", views.LoggedInUserAPIView.as_view(), name="api.me"),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path("api/", include(api_url_patterns)),
    # Swagger URLs
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-schema"),
]
