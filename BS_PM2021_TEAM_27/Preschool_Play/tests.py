from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase, Client, tag
from .models import *
from datetime import datetime
from . import views
# py manage.py test
# Create your tests here.


#@tag('unit-test')
class TestUserProfileModel(TestCase):
    def test_was_born_recently_with_negative_age(self):
        past_user = UserProfile(user=None, address='asd', age=-5, points=0, type='parent', is_admin=False,
                                suspension_time=datetime.now())
        self.assertIs(past_user.was_born_recently_for_parent(), False)

    def test_was_born_recently_with_zero_age(self):
        zero_user = UserProfile(user=None, address='asd', age=0, points=0, type='parent', is_admin=False,
                                suspension_time=datetime.now())
        self.assertIs(zero_user.was_born_recently_for_parent(), False)

    def test_was_born_recently_with_positive_age_less_then_18(self):
        user = UserProfile(user=None, address='asd', age=5, points=0, type='parent', is_admin=False,
                           suspension_time=datetime.now())
        self.assertIs(user.was_born_recently_for_parent(), False)

    def test_was_born_recently_with_positive_age_greater_then_18(self):
        user = UserProfile(user=None, address='asd', age=25, points=0, type='parent', is_admin=False,
                           suspension_time=datetime.now())
        self.assertIs(user.was_born_recently_for_parent(), True)

    def test_new_profile_is_not_authorized_by_default(self):
        user = UserProfile(user=None, address='asd', age=25, points=0, type='parent', is_admin=False,
                           suspension_time=datetime.now())
        self.assertEquals(user.auth, False, 'new user should not be authenticated by default')


#@tag('unit-test')
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


#@tag('unit-test')
class TestSearchUserView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Qwerty246')
        self.user.save()

    def test_non_admin_access_denial(self):
        self.profile = UserProfile(user=self.user, is_admin=False)
        self.profile.save()
        self.client = Client()
        self.client.login(username='testuser', password='Qwerty246')
        data = {'fname': 'fname', 'lname': 'lname'}
        response = self.client.post(reverse('Preschool_Play:search-user'), data=data)
        self.assertTemplateUsed(response, 'Preschool_Play/error.html')

    def test_search_existing_user(self):
        self.profile = UserProfile(user=self.user, is_admin=True)
        self.profile.save()
        self.client = Client()
        self.client.login(username='testuser', password='Qwerty246')
        user2 = User.objects.create_user(username='nuser', password='Qwerty246', first_name='nuser', last_name='luser')
        user2.save()
        profile2 = UserProfile(user=user2, is_admin=False)
        profile2.save()
        data = {'fname': 'nuser', 'lname': 'luser'}
        response = self.client.post(reverse('Preschool_Play:search-user'), data=data)
        self.assertTemplateUsed(response, 'Preschool_Play/search-user.html')
        self.assertContains(response, 'nuser')


#@tag('unit-test')
class TestMediaView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Qwerty246')
        self.user.save()
        self.profile = UserProfile(user=self.user, is_admin=True)
        self.profile.save()
        self.client = Client()
        self.client.login(username='testuser', password='Qwerty246')

    def test_with_add_media(self):
        response = self.client.get(reverse('Preschool_Play:add-media'))
        self.assertEqual(response.status_code, 200)
        add_media = Media(name='name', path='www/rrr/ttt', type='picture')
        add_media.save()
        self.assertContains(response, "Add Media")

    def test_with_delete_media(self):
        response = self.client.get(reverse('Preschool_Play:delete-media'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete Media")


#@tag('unit-test')
class TestUrl(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_Preschool_Play_show_suspend_user_url_is_resolved(self):
        url = reverse('Preschool_Play:show-suspend-user')
        self.assertEqual(resolve(url).func, views.show_suspend_user)

    def test_Preschool_Play_add_media_url_is_resolved(self):
        url = reverse('Preschool_Play:add-media')
        self.assertEqual(resolve(url).func, views.add_media)

    def test_Preschool_Play_delete_media_url_is_resolved(self):
        url = reverse('Preschool_Play:delete-media')
        self.assertEqual(resolve(url).func, views.delete_media)