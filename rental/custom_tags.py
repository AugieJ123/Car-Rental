# custom_tags.py
from django import template

register = template.Library()


@register.simple_tag
def is_active(current_title, target_title):
    return "active" if current_title == target_title else ""
