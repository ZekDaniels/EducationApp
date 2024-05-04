from rest_framework import serializers
from education.models import Science, Lesson
from utilities.serializers import ErrorNameMixin

class ScienceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Science
        fields = "__all__"

        
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
        

