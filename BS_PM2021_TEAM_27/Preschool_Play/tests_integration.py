from django.test import TestCase, Client, tag
from django.urls import reverse, resolve
from . import views
from .models import *


@tag('unit-test')
class TestIntegration(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user('admin', 'admin@test.com')
        self.admin_user.set_password('qwerty246')
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()
        self.admin_profile = UserProfile(user=self.admin_user, is_admin=True)
        self.admin_profile.save()
        self.teacher = User.objects.create_user(username='teacher1')
        self.teacher.set_password('qwerty246')
        self.teacher.save()
        self.teacher_profile = UserProfile(user=self.teacher, type='teacher')
        self.teacher_profile.save()
        self.kg = Kindergarten(name='mypreschool', teacher=self.teacher_profile)
        self.kg.save()
        self.user = User(username='user1')
        self.user.set_password('qwerty246')
        self.user.save()
        self.profile = UserProfile(user=self.user, type='parent', auth=True)
        self.profile.save()
        self.kid = Child(name='kid2', parent=self.profile, teacher=self.teacher_profile, kindergarten=self.kg,
                         auth=True)
        self.kid.save()
        self.client = Client()
        self.client.login(username='user1', password='qwerty246')

    def test_login_then_add_and_delete_new_child(self):
        response = self.client.get(reverse('Preschool_Play:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add Child")
        response = self.client.get(reverse('Preschool_Play:create-child'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Name child")
        form = response.context['form']
        data = form.initial
        data['name_child'] = 'John'
        data['teacher'] = 'teacher1'
        data['kindergarten'] = 'mypreschool'
        response = self.client.post(reverse('Preschool_Play:create-child'), data=data)
        child = Child.objects.filter(name='John', teacher=self.teacher.id, kindergarten=self.kg.id)
        self.assertTrue(len(child) > 0)
        response = self.client.get(reverse('Preschool_Play:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete Child")
        response = self.client.get(reverse('Preschool_Play:delete-user'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Child")
        form = response.context['form']
        choice = None
        for x in form.fields['child']._get_choices():
            if x[0] != '':
                if x[1] == child[0].__str__():
                    choice = x
        data = form.initial
        data['child'] = choice[0]
        data['password'] = 'qwerty246'
        response = self.client.post(reverse('Preschool_Play:delete-user'), data=data)
        child = Child.objects.filter(name='John', teacher=self.teacher.id, kindergarten=self.kg.id)
        self.assertTrue(len(child) == 0)

    def test_register_as_teacher_and_add_kindergarten_and_parent_register_his_child_to_this_kindergarten(self):
        self.client.logout()
        # unregistered user go to main page
        response = self.client.get(reverse('Preschool_Play:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign-Up")
        # go to sign up
        response = self.client.get(reverse('Preschool_Play:new-user'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username")
        # post sign up data
        form = response.context['user_form']
        data = {'username': 'new-teacher', 'password1': 'qwerty256', 'password2': 'qwerty256'}
        response = self.client.post(reverse('Preschool_Play:new-user'), data=data, follow=True)
        # redirected to new profile
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Preschool_Play/new-profile.html')
        # post new profile data
        data = {'address': 'asdf', 'age': 23, 'type': 'teacher'}
        response = self.client.post(reverse('Preschool_Play:new-profile', args=['new-teacher']), data=data, follow=True)
        # authenticate
        up = UserProfile.objects.get(user__username='new-teacher')
        up.auth = True
        up.save()
        # redirected to main page
        self.assertContains(response, 'Sign-In')
        self.assertTrue(len(UserProfile.objects.filter(user__username='new-teacher')) > 0)
        # go to login page
        response = self.client.get(reverse('Preschool_Play:login'))
        self.assertContains(response, 'User name')
        # login
        self.client.force_login(User.objects.get(username='new-teacher'))
        self.assertTrue(User.objects.get(username='new-teacher').is_authenticated)
        response = self.client.get(reverse('Preschool_Play:index'))
        self.assertContains(response, 'Create Kindergarten')
        self.assertTrue(User.objects.get(username='new-teacher').is_authenticated)
        # go to create kindergarten
        response = self.client.get(reverse('Preschool_Play:create-kindergarten'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Name")
        # post data to create kindergarten
        data = {'name': 'new-kinder1'}
        response = self.client.post(reverse('Preschool_Play:create-kindergarten'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(Kindergarten.objects.filter(name='new-kinder1')) > 0)
        self.assertContains(response, "Logout")
        self.client.logout()
        self.client.login(username='user1', password='qwerty246')
        response = self.client.get(reverse('Preschool_Play:create-child'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Name child")
        data = {'name_child': 'ben2', 'teacher': 'new-teacher', 'kindergarten': 'new-kinder1'}
        response = self.client.post(reverse('Preschool_Play:create-child'), data=data, follow=True)
        self.assertTrue(len(Child.objects.filter(name='ben2', parent=self.profile)) > 0)
        response = self.client.get(reverse('Preschool_Play:parent'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ben2")
