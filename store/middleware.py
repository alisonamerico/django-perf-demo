from django.db import connection


class QueryCountMiddleware:
    """
    Captures the number of queries BEFORE any processing.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request._app_query_start = len(connection.queries)
        response = self.get_response(request)
        request._app_query_end = len(connection.queries)
        return response
