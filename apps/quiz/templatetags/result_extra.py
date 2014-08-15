import datetime

from django import template

register = template.Library()


@register.filter
def unix_to_date(unix_date):
    return datetime.datetime.fromtimestamp(int(unix_date)).strftime('%Y-%m-%d')


@register.filter
def unix_to_time(unix_date):
    return datetime.datetime.strptime(
        str(datetime.datetime.fromtimestamp(int(unix_date))), "%Y-%m-%d %H:%M:%S"
    ).time()


@register.filter
def unix_to_day(unix_date):
    datetime.datetime.fromtimestamp(int(unix_date)).strftime("%A, %d. %B %Y")
