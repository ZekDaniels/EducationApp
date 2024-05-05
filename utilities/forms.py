from django import forms

STYLES = {
     "else": {
        'class': 'form-control'
    }
}

class DateInput(forms.DateInput):
    input_type = 'date'

class StyledFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        self._styles = STYLES
        
        super().__init__(*args, **kwargs)
        for name in self.fields:
            if self.fields[name].required is True:
                    print(self.fields[name].__dict__)
                    self.fields[name].label +="*"
            if hasattr(self, "FIELDS"):
                if name in self.FIELDS:
                    self.fields[name].widget.attrs.update(self.FIELDS[name])
            if self.fields[name].widget.__class__.__name__ in self._styles:
                self.fields[name].widget.attrs.update(self._styles[self.fields[name].widget.__class__.__name__])
            else:
                self.fields[name].widget.attrs.update(self._styles["else"])
                


class DisableForm(forms.ModelForm, StyledFormMixin):
    
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs['disabled'] = True