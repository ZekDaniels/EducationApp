from django.db import models
from django.contrib.auth.models import User
from django.db import transaction

from utilities.models import BaseModel
from user.utils import resize_image
# Create your models here.

class Profile(BaseModel):
    """
    This model represents the profile info of Internal Personals.
    """
       
    student = 'student'
    teacher = 'teacher'
    admin = 'admin'
    
    USER_ROLE_CHOICES = ((student, ("Öğrenci")), (teacher, ("Öğretmen")), (admin,("Yönetici")))    
       
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_image = models.ImageField(("Profil Resmi"), upload_to='images/profiles/', null=True, blank=True,
                              help_text=("Lütfen kare profil resminizi kare olacak şekilde yükleyin, yoksa fotoğrafınız kırpılacaktır."))
    namesurname = models.CharField(("Ad Soyad"), max_length=200, default="")
    phone_number = models.CharField(("Telefon Numarası"), max_length=50, blank=False, null=True)
    address = models.TextField(("Adres"), blank=True, null=True)
    student_number = models.CharField(("Öğrenci Numarası"), max_length=9, blank=False, null=False, unique=True, db_index=True)
    identification_number = models.CharField(("TC Kimlik No"), max_length=11, blank=True, null=True)
    user_role = models.CharField(("Kullanıcı Rolü"), max_length=17, choices=USER_ROLE_CHOICES, default=student)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    __image=None

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profiller'

    def __init_(self, *args, **kwargs):
        super().__init_(*args, **kwargs)
        self.__image = self.user_image

    def __str__(self):
        model_text = f"{self.namesurname} | {self.user.username}"
        if self.is_allowed_user():
            model_text = f"{model_text} {self.get_user_role_display()}"
        return model_text

    def save(self, *args, **kwargs):
        """
        Crop image before sending to Amazon, thanks to:
        https://blog.soards.me/posts/resize-image-on-save-in-django-before-sending-to-amazon-s3/
        https://bhch.github.io/posts/2018/12/django-how-to-editmanipulate-uploaded-images-on-the-fly-before-saving/
        """
        # check if the image field is changed
        if self.user_image and self.user_image != self.__image:
            self.user_image = resize_image(self.user_image, 512, 512)
            self.user.save()

        super().save(*args, **kwargs)

    @staticmethod
    def get_read_only_fields():
        return ['student_number', 'identification_number']
    
    def student_permitted(self):
        allowed_user_roles = (Profile.admin, Profile.student)
        student_permitted = self.user_role in allowed_user_roles
        return student_permitted

    def is_allowed_simple(self):
        allowed_simple_roles = (Profile.admin, Profile.student)
        is_allowed_simple = self.user_role in allowed_simple_roles
        return is_allowed_simple