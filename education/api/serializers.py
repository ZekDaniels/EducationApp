from rest_framework import serializers

from education.models import Lesson
from utilities.serializers import ErrorNameMixin
from education.models import LessonStep, LessonStepFile, LessonStudent
from user.api.serializers import ProfileListSerializer        
from user.models import Profile
        
class LessonListSerializer(serializers.ModelSerializer):
    
    teacher = ProfileListSerializer(read_only=True)
    semester_humanize = serializers.CharField(source='get_semester_display')
    
    class Meta:
        model = Lesson
        exclude = ['created_at', 'updated_at']

class LessonCreateSerializer(serializers.ModelSerializer, ErrorNameMixin):


    class Meta:
        model = Lesson
        exclude = ['created_at','updated_at']


    def validate_teacher(self, data):
        validated_data = super().validate(data)
        if validated_data.user_role != Profile.teacher:
            raise serializers.ValidationError('Dersler sadece öğretmenlere atanabilir.')
           
        return validated_data
        
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
        

class LessonStepListSerializer(serializers.ModelSerializer):
    
    files = LessonStepFileListSerializer(read_only=True, many=True)

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

class LessonStudentListSerializer(serializers.ModelSerializer):
    
    lesson = LessonListSerializer(read_only=True)
    student = ProfileListSerializer(read_only=True)
    
    class Meta:
        model = LessonStudent
        exclude = ['created_at', 'updated_at']

class LessonStudentCreateSerializer(serializers.ModelSerializer):
    
    def validate_student(self, data):
        validated_data = super().validate(data)
        if validated_data.user_role != Profile.student:
            raise serializers.ValidationError('Derslere sadece öğrenciler atanabilir.')
           
        return validated_data

    class Meta:
        model = LessonStudent
        exclude = ['created_at','updated_at']
        
    def create(self, validated_data):
        data = super().create(validated_data) 
        return data
