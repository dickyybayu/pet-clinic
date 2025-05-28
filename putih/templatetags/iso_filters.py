from datetime import datetime
from django import template

register = template.Library()

@register.filter
def parse_iso(value):
    if isinstance(value, str):
        try:
            dt_obj = datetime.fromisoformat(value.replace("Z", "")) 
            return dt_obj 
        except ValueError:
            return value 
    return value