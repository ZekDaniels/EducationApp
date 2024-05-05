from django import template

register = template.Library()

@register.filter
def student_permitted(obj):
   return obj.student_permitted()

@register.filter
def teacher_permitted(obj):
   return obj.teacher_permitted()

@register.filter
def admin_permitted(obj):
   return obj.admin_permitted()
