from django import forms

STYLES = {
     "else": {
        'class': 'form-control'
    }
}

class DateInput(forms.DateInput):
    input_type = 'date'

class StyledFormMixin(forms.Form):
    def __init__(self, styles=STYLES, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            if self.fields[name].required is True:
                    self.fields[name].label +="*"
            if hasattr(self, "FIELDS"):
                if name in self.FIELDS:
                    self.fields[name].widget.attrs.update(self.FIELDS[name])
            # add some special classes depend on the element
            if self.fields[name].widget.__class__.__name__ in styles:
                self.fields[name].widget.attrs.update(styles[self.fields[name].widget.__class__.__name__])
            else:
                self.fields[name].widget.attrs.update(styles["else"])

class DisableForm(forms.ModelForm, StyledFormMixin):
    
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs['disabled'] = True