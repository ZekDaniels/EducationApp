from education.api.serializers import *
from django.db import transaction
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics

from utilities.views import QueryListAPIView

class LessonListAPIView(QueryListAPIView):
   
    # custom_related_fields = ['lessonstep_set', 'lessonstudent_set']
    custom_related_fields = ['teacher']
    # queryset = Lesson.objects.select_related(*custom_related_fields).all()
    queryset = Lesson.objects.all()
    serializer_class = LessonListSerializer
    filter_backends = [OrderingFilter, SearchFilter]

    ordering_fields = "__all__"
    search_fields = ['code', 'class_name']


class LessonCreateAPI(generics.CreateAPIView):
    
    queryset = Lesson.objects.all()
    serializer_class = LessonCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile, updated_by=self.request.user.profile)

class LessonUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Lesson.objects.all()
    serializer_class = LessonCreateSerializer

    def destroy(self, request, *args, **kwargs):
    
        instance = self.get_object()
        with transaction.atomic(): 
            return super().destroy(request, *args, **kwargs)

class LessonStepListAPIView(QueryListAPIView):
        
    custom_related_fields = ['lesson']    
    queryset = LessonStep.objects.all()
    serializer_class = LessonStepListSerializer
    filter_backends = [OrderingFilter, SearchFilter]

    ordering_fields = "__all__"
    search_fields = ['lesson', 'step_name']
        

class LessonStepCreateAPI(generics.CreateAPIView):
    
    queryset = LessonStep.objects.all()
    serializer_class = LessonStepCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile, updated_by=self.request.user.profile)

class LessonStepUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = LessonStep.objects.all()
    serializer_class = LessonStepCreateSerializer

    def destroy(self, request, *args, **kwargs):
    
        instance = self.get_object()
        return super().destroy(request, *args, **kwargs)
        
class LessonStepFileListAPIView(QueryListAPIView):
        
    custom_related_fields = ['lesson_step']    
    queryset = LessonStepFile.objects.all()
    serializer_class = LessonStepFileListSerializer
    filter_backends = [OrderingFilter, SearchFilter]

    ordering_fields = "__all__"
    search_fields = ['lesson_step', 'file_name']

class LessonStepFileCreateAPI(generics.CreateAPIView):
    
    queryset = LessonStepFile.objects.all()
    serializer_class = LessonStepFileCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile, updated_by=self.request.user.profile)
    
class LessonStepFileUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = LessonStepFile.objects.all()
    serializer_class = LessonStepFileCreateSerializer

    def destroy(self, request, *args, **kwargs):
    
        instance = self.get_object()
        return super().destroy(request, *args, **kwargs)
    
class LessonStudentListAPIView(QueryListAPIView):
    
    custom_related_fields = ['lesson', 'student']    
    queryset = LessonStudent.objects.all()
    serializer_class = LessonStudentListSerializer
    filter_backends = [OrderingFilter, SearchFilter]

    ordering_fields = "__all__"
    search_fields = ['lesson', 'student']
    
class LessonStudentCreateAPI(generics.CreateAPIView):
        
    queryset = LessonStudent.objects.all()
    serializer_class = LessonStudentCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.profile, updated_by=self.request.user.profile)
    
class LessonStudentUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = LessonStudent.objects.all()
    serializer_class = LessonStudentCreateSerializer

    def destroy(self, request, *args, **kwargs):
    
        instance = self.get_object()
        return super().destroy(request, *args, **kwargs)
    

