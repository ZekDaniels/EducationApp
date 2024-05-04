from email.policy import default
from django.db import models
from utilities.models import BaseModel, BaseModelWithUser

class Science(BaseModel):
    name = models.CharField("Bölüm", max_length=255, null=True, blank=True)
    class Meta:
        verbose_name = 'Bölüm'
        verbose_name_plural = 'Bölümler'
    
    def __str__(self):
        return self.name


class Lesson(BaseModelWithUser):
    """
    The classes can take from user(student),
    
    """
    fall = 'fall'
    spring = 'spring'
    summer = 'summer'
    
    SEMESETER_CHOICES = ((fall, ("Güz")), (spring, ("Bahar")), (summer, ("Yaz")), )

    class Meta:
        verbose_name = 'Öğrenicin Dersi'
        verbose_name_plural = 'Öğrencinin Dersleri'
        ordering = ['semester', 'code']

        
        
    code = models.CharField("Ders Kodu", max_length=20, unique=True, null=False, blank=False)
    class_name = models.CharField("Dersin Adı", max_length=255)
    semester = models.PositiveIntegerField("Dönem", choices= SEMESETER_CHOICES, default=fall)
    science = models.ForeignKey(Science, on_delete=models.CASCADE, null=False, blank=False)

    credit = models.FloatField("Kredi", null=True, blank=True)
    link = models.URLField("Ders İçeriği Linki", max_length=500, null=True, blank=True)
    
    
    def __str__(self):
        return self.code+" - "+self.class_name+" --> "+ self.semester
