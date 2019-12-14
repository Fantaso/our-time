from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


# FILTERS
# if no name, default is function.__name__
@register.filter(name='method_name', is_safe=True)
@stringfilter
def _func_name(value, arg):
    return _func_name.__name__


# better for datetime objects
@register.filter(expects_localtime=True)
def _my_date_format(value):
    try:
        return 9 <= value.hour < 17
    except AttributeError:
        return ''


# TAGS
# it accepts as mny arguments as wanted
# it passes throught a conditional_escape() to autoescape if necessary
def my_tag(a, b, *args, **kwargs):
    warning = kwargs['warning']
    profile = kwargs['profile']
    return ''
    # called in template like a=123, b="abcd" args=[book.title] kwargs={warning and profile}
    # {% my_tag 123 "abcd" book.title warning=message|lower profile=user.profile %}


# if additional escaping is not wanted takes_context=True in decorator as arg
@register.simple_tag(takes_context=True)
def __current_time(context, format_string):
    timezone = context['timezone']
    return 'your_get_current_time_method(timezone, format_string)'
    # uses a variable name so it can be placed anywhere in the template
    # {% _current_time "%Y-%m-%d %I:%M %p" as the_time %}
    # <p>The time is {{ the_time }}.</p>


# INCLUSION TAGS
@register.inclusion_tag('bulma/components/tag.html')
def show_results(poll):
    choices = poll.choice_set.all()
    return {'choices': choices}


@register.inclusion_tag('bulma/components/link.html', takes_context=True)
def jump_link(context):
    return {
        'link': context['home_link'],
        'title': context['home_title'],
    }
# in template its called:
# {% jump_link %}