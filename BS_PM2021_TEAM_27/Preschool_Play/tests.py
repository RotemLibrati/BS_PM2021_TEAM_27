from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
# py manage.py test
# Create your tests here.



class TestUrl(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
