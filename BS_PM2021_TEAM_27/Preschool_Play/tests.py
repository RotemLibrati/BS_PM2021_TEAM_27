from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase, Client
from .models import UserProfile
from . import views
# py manage.py test
# Create your tests here.


class TestUrl(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_Preschool_Play_show_suspend_user_url_is_resolved(self):
        url = reverse('Preschool_Play:show-suspend-user')
        self.assertEqual(resolve(url).func, views.show_suspend_user)


class TestSuspensionView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Qwerty246')
        self.user.save()
        self.profile = UserProfile(user=self.user, is_admin=True)
        self.profile.save()
        self.client = Client()
        self.client.login(username='testuser', password='Qwerty246')

    def test_show_suspension(self):
        response = self.client.get(reverse('Preschool_Play:show-suspend-user'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Users")
        self.assertContains(response, "Suspend user")
        self.assertTemplateUsed(response, 'Preschool_Play/show-suspend-user.html')