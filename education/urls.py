from django.urls import path, include
from education.views import *
app_name = "education"

urlpatterns = [
    path('education/', AdaptationList.as_view(), name="education"),
    path('api/education/', include('education.api.urls')),
]