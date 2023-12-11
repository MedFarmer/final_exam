from django import template

register = template.Library()

"""
    данная функция позволяет разделять суммы на тысячные используя пробел.
"""

@register.filter
def thousands_with_spaces(value):
    try:       
        value = int(value) if isinstance(value, str) else value        
        formatted_value = "{:,}".format(value).replace(",", " ")
        return formatted_value
    except (ValueError, TypeError):
        return value
