from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Adds a CSS class to a given form field
    Usage: {{ form.field_name|add_class:"class_name" }}
    """
    return value.as_widget(attrs={"class": arg})