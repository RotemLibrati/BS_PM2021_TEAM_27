from builtins import super

from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

from .models import Media


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
    set = UserProfile.objects.filter(is_admin=True)
    USERS = list(map(lambda x: (str(x.user), str(x.user)), set))
    receiver = forms.CharField(widget=forms.Select(choices=USERS))
    subject = forms.CharField(max_length=50, initial='message subject')
    body = forms.CharField(max_length=5000, widget=forms.Textarea)
