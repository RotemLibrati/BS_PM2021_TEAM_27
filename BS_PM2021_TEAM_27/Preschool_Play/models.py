from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime

from django.db.models import UniqueConstraint


class UserProfile(models.Model):
    TYPES = (('parent', 'parent'), ('teacher', 'teacher'))
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=100, default='')
    age = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    type = models.CharField(max_length=10, choices=TYPES, default='parent')
    is_admin = models.BooleanField(default=False)
    suspension_time = models.DateTimeField(default=datetime(2000, 1, 1))
    total_minutes = models.FloatField(default=0)
    last_login = models.DateTimeField(default=datetime(2000, 1, 1))
    rank = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    limit = models.DateTimeField(default=datetime(2000, 1, 1))
    auth = models.BooleanField(default=False)

    def was_born_recently_for_parent(self):
        if self.age <= 0:
            return False
        return self.age > 18

    def __str__(self):
        return str(self.user)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent', on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(User, related_name='received', on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=50, blank=True)
    body = models.CharField(max_length=250, blank=True)
    sent_date = models.DateTimeField(auto_now_add=True)
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_receiver = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    is_unread = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.sender}  to  {self.receiver}"


class Media(models.Model):
    TYPES = (('music', 'music'), ('picture', 'picture'))
    name = models.CharField(max_length=20)
    path = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=TYPES, default='picture')

    def __str__(self):
        return f'Name: {self.name}. Path: {self.path}. Type: {self.type}'


class Kindergarten(models.Model):
    name = models.CharField(max_length=50, blank=True, null=False)
    teacher = models.ForeignKey(UserProfile, related_name='teacher', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Child(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey(User, related_name='child', on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(UserProfile, related_name='student', on_delete=models.SET_NULL, null=True)
    suspension_time = models.DateTimeField(default=datetime(2000, 1, 1))
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Name: {self.name}. Parent: {self.parent}'


class Score(models.Model):
    child = models.ForeignKey(Child, related_name='score', on_delete=models.SET_NULL, null=True)
    game = models.CharField(max_length=50, blank=True, null=False)
    amount = models.IntegerField(default=0)
    comment = models.CharField(max_length=250, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f'Child: {self.child.__str__()}, Amount: {self.amount.__str__()}, Comment: {self.comment}, Date: {self.date.__str__()}'


class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=256)
    seen = models.BooleanField(default=False)


class Note(models.Model):
    teacher = models.ForeignKey(User, related_name='note', on_delete=models.SET_NULL, null=True)
    child = models.ForeignKey(Child, related_name='note', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    subject = models.CharField(max_length=250, blank=True, null=True)
    body = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'Child: {self.child}. Subject: {self.subject}. Date: {self.date}.'
