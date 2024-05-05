from django.contrib import admin
from education.models import *
# Register your models here.

admin.site.register(Lesson)
admin.site.register(LessonStep)
admin.site.register(LessonStepFile)
admin.site.register(LessonStudent)
