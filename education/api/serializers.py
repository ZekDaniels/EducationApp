from rest_framework import serializers

from education.models import Lesson
from utilities.serializers import ErrorNameMixin
from education.models import LessonStep, LessonStepFile, LessonStudent
        
class LessonListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        exclude = ['created_at', 'updated_at']

class LessonCreateSerializer(serializers.ModelSerializer, ErrorNameMixin):

    credit = serializers.CharField(default=None, required=False, allow_blank=True, allow_null=True,)

    class Meta:
        model = Lesson
        exclude = ['created_at','updated_at']

    def validate_credit(self, data):  
        validated_data = super().validate(data)

        if validated_data['credit'] is None:
            raise serializers.ValidationError(("Kredi tamsayı veya virgüllü sayı olmalı, AKTS tam sayı olmalı. Her iki değerden birisi mutlaka girilmeli.")) 
           
        return validated_data
        
    def create(self, validated_data):
        data = super().create(validated_data) 
        return data
        

class LessonStepListSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonStep
        exclude = ['created_at', 'updated_at']
        
class LessonStepCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonStep
        exclude = ['created_at','updated_at']
        
    def create(self, validated_data):
        data = super().create(validated_data) 
        return data
    
class LessonStepFileListSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonStepFile
        exclude = ['created_at', 'updated_at']
        
class LessonStepFileCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LessonStepFile
        exclude = ['created_at','updated_at']
        
    def create(self, validated_data):
        data = super().create(validated_data) 
        return data

class LessonStudentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonStudent
        exclude = ['created_at', 'updated_at']

class LessonStudentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonStudent
        exclude = ['created_at','updated_at']
        
    def create(self, validated_data):
        data = super().create(validated_data) 
        return data
