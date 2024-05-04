
from django.urls import path
from education.api.views import *
from education.views import *
urlpatterns = [
     
     path('student_classes_list', LessonListAPIView.as_view(), name="student_classes_list_api"),
     path('student_class', LessonCreateAPI.as_view(), name="student_class_create_api"),
     path('student_class/<int:pk>', LessonUpdateAPI.as_view(), name="student_class_update_api"),
     path('science_list', ScienceListView.as_view(), name="science_list_api"),
]
 
