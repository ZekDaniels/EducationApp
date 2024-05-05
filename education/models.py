from email.policy import default
from django.db import models
from utilities.models import BaseModelWithUser
from django.urls import reverse

from user.models import Profile
class Lesson(BaseModelWithUser):
    """
    The classes can take from user(student),
    
    """
    fall = 'fall'
    spring = 'spring'
    summer = 'summer'
    
    level1 = 'level1'
    level2 = 'level2'
    level3 = 'level3'
    level4 = 'level4'
    

    SEMESETER_CHOICES = ((fall, ("Güz")), (spring, ("Bahar")), (summer, ("Yaz")), )
    LEVEL_CHOICES = ((level1, ("1. Seviye")), (level2, ("2. Seviye")), (level3, ("3. Seviye")), (level4, ("4. Seviye")), )

    class Meta:
        verbose_name = 'Ders'
        verbose_name_plural = 'Dersler'
        ordering = ['semester', 'code']
        
    code = models.CharField("Ders Kodu", max_length=20, unique=True, null=False, blank=False)
    class_name = models.CharField("Dersin Adı", max_length=255)
    semester = models.PositiveIntegerField("Dönem", choices= SEMESETER_CHOICES, default=fall)
    level = models.PositiveIntegerField("Seviye", choices= LEVEL_CHOICES, default=level1)
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Öğretmen", related_name="taught_lessons")

    
    def __str__(self):
        return self.code+" - "+self.class_name+" --> "+ self.get_semester_display()
    
class LessonStudent(BaseModelWithUser):
    """
    The classes can take from user(student),
    
    """
    class Meta:
        verbose_name = 'Ders Öğrencisi'
        verbose_name_plural = 'Ders Öğrencileri'
        ordering = ['lesson', 'student']
        
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Ders", related_name="students")
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Öğrenci", related_name="enrolled_lessons")
    link = models.URLField("Ders İçeriği Linki", max_length=500, null=True, blank=True)
    
    
    def __str__(self):
        return self.lesson.code+" - "+self.lesson.class_name+" --> "+ self.student.namesurname


    def get_absolute_url(self):
        return reverse('lesson_student_detail', args=[str(self.id)])
    
class LessonStep(BaseModelWithUser):
    
    class Meta:
        verbose_name = 'Ders Aşaması'
        verbose_name_plural = 'Ders Aşamaları'
        ordering = ['lesson', 'step_number']
        unique_together = ['lesson', 'step_number']
    
    name = models.CharField("Aşama", max_length=255)
    content = models.TextField("Aşama İçeriği", null=True, blank=True)
    step_number = models.PositiveIntegerField("Aşama Numarası", default=1)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Ders", related_name="steps")
    
    def __str__(self):
        return str(self.step_number)+"- "+self.name
    
class LessonStepFile(BaseModelWithUser):
    
    class Meta:
        verbose_name = 'Ders Aşama Dosyası'
        verbose_name_plural = 'Ders Aşama Dosyaları'
        ordering = ['step', 'file']
        
    step = models.ForeignKey(LessonStep, on_delete=models.CASCADE, verbose_name="Aşama", related_name="files")
    file = models.FileField("Dosya", upload_to='lessons/files/', null=False, blank=False)
    
    def __str__(self):
        return self.step.name+" - "+self.file.name
    
    def get_absolute_url(self):
        return reverse('lesson_step_files_detail', args=[str(self.id)])