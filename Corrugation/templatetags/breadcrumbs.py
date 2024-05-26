from django import template
from django.urls import resolve, Resolver404
from urllib.parse import unquote

register = template.Library()


@register.simple_tag(takes_context=True)
def breadcrumbs(context):
    request = context['request']
    path = unquote(request.path)
    parts = path.strip('/').split('/')

    breadcrumb_urls = []
    breadcrumb_path = ''
    for part in parts:
        breadcrumb_path += f'/{part}'
        try:
            resolved = resolve(breadcrumb_path)
            name = resolved.url_name if resolved.url_name else part
        except Resolver404:
            name = part
        breadcrumb_urls.append((name, breadcrumb_path))

    return breadcrumb_urls
