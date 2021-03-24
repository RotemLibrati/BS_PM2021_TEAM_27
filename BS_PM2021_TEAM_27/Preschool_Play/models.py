from django.contrib.auth.models import User
from django.db import models


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


class Child(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    suspended = models.BooleanField(default=False)