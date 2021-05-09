from builtins import super
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from .models import UserProfile, Child
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


class CreateUserForm(UserCreationForm):  # create user - django
    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2',
                  )

        def save(self, commit=True):
            user = super(CreateUserForm, self).save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']

            if commit:
                user.save()
            return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address', 'age', 'type')


class ChildForm(forms.Form):
    name_child= forms.CharField(max_length=30)
    teacher = forms.CharField()
    kindergarten = forms.CharField()


class DeleteUserForm(forms.Form):
    def __init__(self, set1, *args, **kwargs):
        super(DeleteUserForm, self).__init__(*args, **kwargs)
        self.fields['child'].queryset = set1

    child = forms.ModelChoiceField(queryset=Child.objects.all())
    password = forms.CharField(widget=forms.PasswordInput)


class DeletePrimaryUserForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

