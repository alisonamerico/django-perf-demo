from django.db import connection


def query_count(request):
    try:
        start = getattr(request, '_app_query_start', 0)
        return {'query_count': len(connection.queries) - start}
    except:
        return {'query_count': 0}
