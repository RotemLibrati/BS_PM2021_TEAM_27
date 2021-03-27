from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime


class UserProfile(models.Model):
    TYPES = (('parent', 'parent'), ('teacher', 'teacher'))
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, blank=True, null=True)
    son = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='dad')
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



class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent', on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(User, related_name='received', on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=50, blank=True)
    body = models.CharField(max_length=250, blank=True)
    sent_date = models.DateTimeField(auto_now_add=True)
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_receiver = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sender + ' to ' + self.receiver)

