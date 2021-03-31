from django import forms
from .models import Media



class AddMediaForm(forms.Form):
    TYPE = (('picture', 'Picture'), ('music', 'Music'))
    name = forms.CharField(max_length=20)
    path = forms.CharField(max_length=200)
    type = forms.CharField(widget=forms.Select(choices=TYPE))
