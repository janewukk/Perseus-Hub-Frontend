from django import template

register = template.Library()

@register.filter(name='to_priority_string')
def convert(value):
    if str(value) == '0':
    	return "low"
    if str(value) == '1':
    	return "medium"
    if str(value) == '2':
    	return "high"