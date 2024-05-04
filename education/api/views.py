from education.api.serializers import *
from django.db import transaction
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics

from utilities.views import QueryListAPIView

class LessonListAPIView(QueryListAPIView):
   
    custom_related_fields = ["adaptation", "adaptation_class"]
    queryset = Lesson.objects.select_related(*custom_related_fields).all()
    serializer_class = LessonListSerializer
    filter_backends = [OrderingFilter, SearchFilter]

    ordering_fields = "__all__"
    search_fields = ['code', 'class_name']


class LessonCreateAPI(generics.CreateAPIView):
    
    queryset = Lesson.objects.all()
    serializer_class = LessonCreateSerializer

class LessonUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Lesson.objects.all()
    serializer_class = LessonCreateSerializer

    def destroy(self, request, *args, **kwargs):

        
        instance = self.get_object()
        if not request.user.profile.is_allowed_user():
            if instance.adaptation.is_closed:
                raise serializers.ValidationError(("Bu intibak başvurusu kapatılmış, değiştirmek istediğinize eminseniz tekrar hocanıza başvurun."))
            
            if instance.adaptation.user != request.user:
                raise serializers.ValidationError(("Bu kullanıcının intibak başvurusunu değiştiremezsiniz."))
        with transaction.atomic(): 
            try:
                confirmation = instance.adaptation.confirmations.get(adaptation_class=instance.adaptation_class)  
            except:
                confirmation = None
            if confirmation:
                instance.adaptation.confirmations.get(adaptation_class=instance.adaptation_class).delete()
            return super().destroy(request, *args, **kwargs)
