from django import template

register = template.Library()


@register.filter
def add_percent(value, percent):
    try:
        value = float(value)
        percent = float(percent)
        return value + (value * percent / 100)
    except (ValueError, TypeError):
        return value


@register.filter
def floatformat(value, decimals):
    try:
        return f"{float(value):.{decimals}f}"
    except (ValueError, TypeError):
        return value
