from email.policy import default
from django.db import models
from utilities.models import BaseModelWithUser

class Lesson(BaseModelWithUser):
    """
    The classes can take from user(student),
    
    """
    fall = 'fall'
    spring = 'spring'
    summer = 'summer'
    

    SEMESETER_CHOICES = ((fall, ("Güz")), (spring, ("Bahar")), (summer, ("Yaz")), )

    class Meta:
        verbose_name = 'Ders'
        verbose_name_plural = 'Dersler'
        ordering = ['semester', 'code']
        
    code = models.CharField("Ders Kodu", max_length=20, unique=True, null=False, blank=False)
    class_name = models.CharField("Dersin Adı", max_length=255)
    semester = models.PositiveIntegerField("Dönem", choices= SEMESETER_CHOICES, default=fall)

    link = models.URLField("Ders İçeriği Linki", max_length=500, null=True, blank=True)
    
    
    def __str__(self):
        return self.code+" - "+self.class_name+" --> "+ self.get_semester_display()
