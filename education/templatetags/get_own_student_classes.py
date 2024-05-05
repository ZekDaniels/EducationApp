from django import template
register = template.Library()

@register.filter
def get_own_student_classes(obj, education):
   return obj.get_own_student_classes(education).order_by("education_class")


@register.filter
def get_own_student_classes_count(obj, education):
   return obj.get_own_student_classes(education).count()

@register.filter
def get_education_class_list_akts_sum(obj):
   return obj.get_education_class_list_akts_sum()