from django import template

register = template.Library()


@register.filter()
def censor(text):
   filtered_text = text.replace('редиска', 'р***')

   return f'{filtered_text}'