from django import forms
from .models import Inquiry

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['message', 'email']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'maxlength': 500}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            self.fields['email'].widget.attrs['readonly'] = True