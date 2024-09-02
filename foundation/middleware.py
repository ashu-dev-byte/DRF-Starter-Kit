from django.db import connections
from django.utils.deprecation import MiddlewareMixin


class QueryCountDebugMiddleware(MiddlewareMixin):
    """
    This middleware logs the number of queries executed and the total time taken for each request (that returns a status code of 200).
    Note: It does not support multi-database configurations.

    django-debug-toolbar monkeypatches the connection's cursor wrapper,
    adding extra information to each item in connection.queries. The query
    execution time is recorded under the key "duration" (in milliseconds),
    instead of "time" (which is in seconds).
    """

    def process_response(self, request, response):
        GREEN, END = "\033[92m", "\033[0m"

        if response.status_code == 200:
            for connection in connections:
                total_time = 0
                for query in connections[connection].queries:
                    query_time = query.get("time")
                    if query_time is None:
                        query_time = query.get("duration", 0) / 1000
                    total_time += float(query_time)

                print(
                    f"{GREEN}{connection}: {len(connections[connection].queries)} queries run,"
                    f" total {total_time} seconds {END}"
                )
        return response
