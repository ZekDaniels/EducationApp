from django.urls import path, include
from education.views import *
app_name = "education"

urlpatterns = [
    path('dersler/', LessonListView.as_view(), name="lesson_list"),
    path('api/education/', include('education.api.urls')),
]