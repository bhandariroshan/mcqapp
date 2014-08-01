import datetime

from django import template

register = template.Library()


@register.filter
def unix_to_date(unix_date):
    return datetime.datetime.fromtimestamp(int(unix_date)).strftime('%Y-%m-%d')
