from pyexpat import model
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from user.models import Profile
from utilities.forms import StyledFormMixin as BaseStyledFormMixin

STYLES = {
    "CheckboxInput": {
        'class': 'custom-control-input'
    },
     "else": {
        'class': 'form-control'
    }
}

class StyledFormMixin(BaseStyledFormMixin):
    def __init__(self, *args, **kwargs):
        self.styles = STYLES
        super().__init__(*args, **kwargs)
        
class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)
    

class UserPasswordResetForm(StyledFormMixin, PasswordResetForm):
     
    FIELDS = {}

class UserSetPasswordForm(StyledFormMixin, SetPasswordForm):

    FIELDS = {}


class NewUserForm(UserCreationForm, StyledFormMixin):
    
    email = forms.EmailField(required=True, label='E-Mail Adresi')
                     
    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class NewProfileForm(forms.ModelForm, StyledFormMixin):
    
    is_teacher = forms.BooleanField(required=False, label='Öğretmen Adayıyım', widget=forms.CheckboxInput(attrs={'class':'custom-control-input'}))

    class Meta:
        model = Profile
        fields = ['namesurname']

class ProfileUpdateForm(NewProfileForm):

    def clean_number(self):
        number = self.cleaned_data['number']

        if not number.isdigit():
            raise ValidationError('Sadece numerik karakter girebilirsiniz.')

        if len(number) != 9:
            raise ValidationError('Eksik veya fazla karakter girdiniz.')
        
        if Profile.objects.filter(number=number).count() > 0:
            raise ValidationError('Bu numara ile daha önce kayıt olunmuş.')
        return number
    
    def clean_identification_number(self):
        identification_number = self.cleaned_data['identification_number']

        if not identification_number.isdigit():
            raise ValidationError('Sadece numerik karakter girebilirsiniz.')

        if len(identification_number) != 11:
            raise ValidationError('Eksik veya fazla karakter girdiniz.')
        
        if Profile.objects.filter(identification_number=identification_number).count() > 0:
            raise ValidationError('Bu numara ile daha önce kayıt olunmuş.')
        return identification_number

    
    class Meta:
        model=Profile
        exclude = ['namesurname', 'phone_number','address','identification_number','number','user_image']

class ProfileAdminForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude = ("created_at", "updated_at")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)