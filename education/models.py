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
    
    class1 = 'class1'
    class2 = 'class2'
    class3 = 'class3'
    class4 = 'class4'
    class5 = 'class5'
    class6 = 'class6'
    class7 = 'class7'
    class8 = 'class8'
    class9 = 'class9'
    class10 = 'class10'
    class11 = 'class11'
    class12 = 'class12'
    

    SEMESETER_CHOICES = ((fall, ("Güz")), (spring, ("Bahar")), (summer, ("Yaz")), )
    CLASS_CHOICES = (
        (class1, ("1. Sınıf")), (class2, ("2. Sınıf")), (class3, ("3. Sınıf")), (class4, ("4. Sınıf")),
        (class5, ("5. Sınıf")), (class6, ("6. Sınıf")), (class7, ("7. Sınıf")), (class8, ("8. Sınıf")),
        (class9, ("9. Sınıf")), (class10, ("10. Sınıf")), (class11, ("11. Sınıf")), (class12, ("12. Sınıf")),
                     )

    class Meta:
        verbose_name = 'Ders'
        verbose_name_plural = 'Dersler'
        ordering = ['semester', 'code']
        
    code = models.CharField("Ders Kodu", max_length=20, unique=True, null=False, blank=False)
    class_name = models.CharField("Dersin Adı", max_length=255)
    semester = models.CharField("Dönem", choices= SEMESETER_CHOICES, default=fall, max_length=10)
    student_class = models.CharField("Sınıf", choices= CLASS_CHOICES, default=class1, max_length=10)
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Öğretmen", related_name="taught_lessons")
    link = models.URLField("Ders İçeriği Linki", max_length=500, null=True, blank=True)

    
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