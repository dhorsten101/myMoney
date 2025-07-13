# monitoring/templatetags/ping_tags.py
from django import template

register = template.Library()


@register.filter
def failed_pings(pings):
	"""Return count of failed ping results"""
	return sum(1 for p in pings if not p.success)
