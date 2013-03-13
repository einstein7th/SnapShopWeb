from django import template

register = template.Library()

@register.filter
def pretty_price(cents):
    return '$' + str(cents / 100) + '.' + str(cents % 100)
