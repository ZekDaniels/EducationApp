
from django.urls import path
from education.api.views import *
from education.views import *
urlpatterns = [
     
     path('lesson_list', LessonListAPIView.as_view(), name="lesson_list_api"),
     path('lesson', LessonCreateAPI.as_view(), name="lesson_create_api"),
     path('lesson/<int:pk>', LessonUpdateAPI.as_view(), name="lesson_update_api"),
]
 
