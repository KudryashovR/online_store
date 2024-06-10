from django import template


register = template.Library()


@register.filter
def remove_trailing_slash(url):
    if url.endswith('/'):
        return url[:-1]

    return url


@register.filter
def media_redirection(media_url):
    return f"/media/{media_url}"
