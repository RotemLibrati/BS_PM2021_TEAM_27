from builtins import super

from django import forms
from django.contrib.auth.models import User

from .models import Media



class AddMediaForm(forms.Form):
    TYPE = (('picture', 'Picture'), ('music', 'Music'))
    name = forms.CharField(max_length=20)
    path = forms.CharField(max_length=200)
    type = forms.CharField(widget=forms.Select(choices=TYPE))


class DeleteMediaForm(forms.Form):
    set = Media.objects.all()
    MEDIA = list(map(lambda x: (str(x.name), str(x.name)), set))
    name = forms.CharField(widget=forms.Select(choices=MEDIA))