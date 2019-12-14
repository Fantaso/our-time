from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


# without takes_context=True args are autoescaped
@register.inclusion_tag('bulma/components/button.html')
def button(action, color, icon, size):
    return {
        'size': size,
        'color': color,
        'icon': icon,
        'action': action,
    }


@register.inclusion_tag('bulma/components/card.html')
def card(title, year, person):
    return {
        'title': title,
        'year': year,
        'person': person,
    }
