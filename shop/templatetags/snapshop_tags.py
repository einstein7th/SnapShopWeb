from django import template
register = template.Library()

def format_price(value_in_cents):
    return "$%.2f" % (int(value_in_cents)/100.0)

def divide(value,divisor):
    return int(value)/int(divisor)

def idify(keyword):
    return keyword.replace(" ","")

register.filter('format_price', format_price)
register.filter('divide', divide)
register.filter('idify', idify)
