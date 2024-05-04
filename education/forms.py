from django import forms

from education.models import Lesson
from utilities.forms import StyledFormMixin as BaseStyledFormMixin

STYLES = {
    "date-input":{
        "class": 'form-control'
    },
     "else": {
        'class': 'form-control'
    }
}

class DateInput(forms.DateInput):
    input_type = 'date'

class StyledFormMixin(BaseStyledFormMixin):
    def __init__(self, styles=STYLES, *args, **kwargs):
        super().__init__(*args, **kwargs, styles=styles)
        

class StudentClassForm(forms.ModelForm, StyledFormMixin):
    
    def __init__(self, *args, **kwargs):
        # user = kwargs.pop('user',None)
        super().__init__(*args, **kwargs)
    class Meta:
        model = Lesson
        exclude = [ 'created_at', 'updated_at']