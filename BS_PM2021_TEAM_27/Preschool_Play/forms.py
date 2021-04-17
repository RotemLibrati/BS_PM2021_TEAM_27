from builtins import super

from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

from .models import Media, Kindergarten


class LoginForm(forms.Form):
    user_name = forms.CharField(initial='')
    password = forms.CharField(widget=forms.PasswordInput(), initial='')


class AddMediaForm(forms.Form):
    TYPE = (('picture', 'Picture'), ('music', 'Music'))
    name = forms.CharField(max_length=20)
    path = forms.CharField(max_length=200)
    type = forms.CharField(widget=forms.Select(choices=TYPE))


class DeleteMediaForm(forms.Form):
    set = Media.objects.all()
    MEDIA = list(map(lambda x: (str(x.name), str(x.name)), set))
    name = forms.CharField(widget=forms.Select(choices=MEDIA))


class MessageForm(forms.Form):
    receiver = forms.CharField()
    subject = forms.CharField(max_length=50, initial='message subject')
    body = forms.CharField(max_length=5000, widget=forms.Textarea)


class KindergartenListForm(forms.Form):
    set = Kindergarten.objects.all()
    KINDERGARTEN = list(map(lambda x: (str(x.name), str(x.name)), set))
    name = forms.CharField(widget=forms.Select(choices=KINDERGARTEN))