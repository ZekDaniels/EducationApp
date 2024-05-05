
from django.urls import path
from education.api.views import *
from education.views import *
urlpatterns = [
     
     path('lesson_list', LessonListAPIView.as_view(), name="lesson_list_api"),
     path('lesson', LessonCreateAPI.as_view(), name="lesson_create_api"),
     path('lesson/<int:pk>', LessonUpdateAPI.as_view(), name="lesson_update_api"),
     
     path('lesson_step_list', LessonStepListAPIView.as_view(), name="lesson_step_list_api"),
     path('lesson_step', LessonStepCreateAPI.as_view(), name="lesson_step_create_api"),   
     path('lesson_step/<int:pk>', LessonStepUpdateAPI.as_view(), name="lesson_step_update_api"),
     
     path('lesson_step_file_list', LessonStepFileListAPIView.as_view(), name="lesson_step_file_list_api"),
     path('lesson_step_file', LessonStepFileCreateAPI.as_view(), name="lesson_step_file_create_api"),
     path('lesson_step_file/<int:pk>', LessonStepFileUpdateAPI.as_view(), name="lesson_step_file_update_api"),
     
     path('lesson_student_list', LessonStudentListAPIView.as_view(), name="lesson_student_list_api"),
     path('lesson_student', LessonStudentCreateAPI.as_view(), name="lesson_student_create_api"),
     path('lesson_student/<int:pk>', LessonStudentUpdateAPI.as_view(), name="lesson_student_update_api"),
]
 
