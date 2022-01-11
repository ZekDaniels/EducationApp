from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

STYLES = {
     "else": {
        'class': 'form-control'
    }
}

class University(models.Model): 
    name = models.CharField("Üniversite", max_length=255)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Üniversite'
        verbose_name_plural = 'Üniversiteler'
    
class Faculty(models.Model):
    name = models.CharField("Fakülte", max_length=255, null=True, blank=True)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, blank=True, null=True, related_name="faculties")

    class Meta:
        verbose_name = 'Fakülte'
        verbose_name_plural = 'Fakülteler'
        
    def __str__(self):
        return self.name

class Science(models.Model):
    name = models.CharField("Bölüm", max_length=255, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, blank=True, null=True, related_name="sciences")
    university = models.ForeignKey(University, on_delete=models.SET_NULL, blank=True, null=True, related_name="sciences")

    class Meta:
        verbose_name = 'Bölüm'
        verbose_name_plural = 'Bölümler'
    
    def __str__(self):
        return self.name

class Adaptation(models.Model):
    
    class Meta:
        verbose_name = 'İntibak'
        verbose_name_plural = 'İntibaklar'
    
    DG = 'dg'
    YG = 'yg'
    YO = 'yo'
    MT = 'mt'
    
    REASON_CHOCIES = (
        (DG, ("Dikey Geçiş")),
        (YG, ("Yatay Geçiş")),
        (YO, ("Yaz Okulu")),
        (MT, ("Mühendislik Tamamlama")),
    )
    SEMESETER_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), )
    YEAR_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), )
    university = models.ForeignKey(University, on_delete=models.DO_NOTHING, verbose_name="Üniversite")    
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING, verbose_name="Fakülte")
    science = models.ForeignKey(Science, on_delete=models.DO_NOTHING, verbose_name="Bölüm")
    reason_for_coming = models.CharField("Geliş Nedeni", max_length=2, choices=REASON_CHOCIES)
    adaptation_year = models.IntegerField("İntibak Sınıfı", choices=YEAR_CHOICES)
    adaptation_semester = models.IntegerField("İntibak Yarıyılı", choices=SEMESETER_CHOICES)
    decision_date = models.DateField("Karar Tarihi", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=("adaptation"), verbose_name="Öğrenci", unique=True)      
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    
    def __str__(self):
        return f"{self.user.profile.namesurname} {self.user.username}"

class AdapatationClass(models.Model):
    """
    The classes added in system,
    """
    SEMESETER_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), )

    class Meta:
        verbose_name = 'İntibak Dersi'
        verbose_name_plural = 'İntibak Dersleri'
    
    code = models.CharField("Ders Kodu", max_length=20, unique=True)
    class_name = models.CharField("Dersin Adı", max_length=255)
    semester = models.IntegerField("Semester", choices= SEMESETER_CHOICES)
    credit = models.IntegerField("Credit")
    akts = models.IntegerField("AKTS")
    is_active = models.BooleanField(("Aktif mi?"), default=True)
    
    def __str__(self):
        return self.code+" - "+self.class_name  

class StudentClass(models.Model):
    """
    The classes can take from user(student),
    """
    SEMESETER_CHOICES = ((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), )

    
    GRADE_CHOICES = (
        (4.0, ("AA")),
        (3.5, ("BA")),
        (3.0, ("BB")),
        (2.5, ("CB")),
        (2.0, ("CC")),
        (1.5, ("DC")),
        (1.0, ("DD")),
        (0.5, ("FD")),
        (0, ("FF")),
    )
    class Meta:
        verbose_name = 'Öğrenicin Dersi'
        verbose_name_plural = 'Öğrencinin Dersleri'
        
    code = models.CharField("Ders Kodu", max_length=20, unique=True)
    class_name = models.CharField("Dersin Adı", max_length=255)
    semester = models.IntegerField("Dönem", choices= SEMESETER_CHOICES, default=1)
    credit = models.IntegerField("Kredi")
    akts = models.IntegerField("AKTS")
    grade = models.FloatField("Not", choices=GRADE_CHOICES, default=4.0)
    adaptation = models.ForeignKey(Adaptation, on_delete=models.CASCADE, related_name=("student_classes"), verbose_name="İntibak")      
    adaptation_class = models.ForeignKey(AdapatationClass, on_delete=models.CASCADE, related_name=("student_classes"), verbose_name="İntibak Dersi")      

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.code+" - "+self.class_name+" --> "+ self.adaptation_class.class_name
    
    
    def get_max_grade(self):
        candidate_classes = StudentClass.objects.filter(adaptation_class=self.adaptation_class)
        candidate_classes.aggregate(Max('grade'))
        max_grade_class = candidate_classes.order_by('-grade').first()
        return max_grade_class.get_grade_display()