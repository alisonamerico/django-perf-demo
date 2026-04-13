from django import template
from django.db import connection

register = template.Library()


@register.simple_tag(takes_context=True)
def query_count_delta_tag(context):
    """Retorna o número de queries executadas desde o início da view (excluindo Debug Toolbar/Silk)."""
    request = context.get('request')
    if request and hasattr(request, '_app_query_start'):
        return len(connection.queries) - request._app_query_start
    return len(connection.queries)
