from django import template
from django.conf import settings

register = template.Library()


is_env_prod = getattr(settings, "ENV") == "prod"


@register.simple_tag
def primary_color():
    return "#5F71DA" if is_env_prod else "#79aec8"


@register.simple_tag
def secondary_color():
    return "#2A3990" if is_env_prod else "#417690"
