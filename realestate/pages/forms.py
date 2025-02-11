from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    full_name=forms.CharField()
    email=forms.EmailField()
    subject=forms.CharField()
    message=forms.CharField()

    class Meta:
        model=Contact
        fields=['full_name','email','subject','message']
