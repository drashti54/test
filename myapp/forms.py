from django import forms
from django.forms import fields
from .models import signup,notes

class signupForm(forms.ModelForm):
    class Meta:
        model=signup
        fields='__all__'
    
class notesForm(forms.ModelForm):
    class Meta:
        model=notes
        fields='__all__'