from django.test import TestCase, Client, tag
from django.urls import reverse, resolve
from . import views
from .models import *
from  django.contrib.auth.hashers import make_password


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
            print(x)
        breakpoint()
        data = form.initial
        data['child'] = choice
        data['password'] = 'qwerty246'
        response = self.client.post(reverse('Preschool_Play:delete-user'), data=data)
        child = Child.objects.filter(name='John', teacher=self.teacher.id, kindergarten=self.kg.id)
        print(child)
        self.assertTrue(len(child) == 0)

    def test_with_no_messages(self):
        c = Client()
        user = User.objects.create_user(username='tester')
        user.set_password('qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        c.force_login(user)
        response = c.get(reverse('Preschool_Play:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Preschool_Play/inbox.html')
        self.assertEquals(len(response.context['messages_received']), 0)
        self.assertEquals(len(response.context['messages_sent']), 0)

    def test_with_message_received(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        user2 = User.objects.create_user(username='tester2', password='qwerty246')
        user2.save()
        user_profile2 = UserProfile.objects.create(user=user2)
        user_profile2.save()
        message = Message(sender=user2, receiver=user, body='hello')
        message.save()
        c.force_login(user)
        response = c.get(reverse('Preschool_Play:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Preschool_Play/inbox.html')
        self.assertEquals(len(response.context['messages_received']), 1)
        self.assertEquals(len(response.context['messages_sent']), 0)

    def test_with_message_sent(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        user2 = User.objects.create_user(username='tester2', password='qwerty246')
        user2.save()
        user_profile2 = UserProfile.objects.create(user=user2)
        user_profile2.save()
        message = Message(sender=user2, receiver=user, body='hello')
        message.save()
        c.force_login(user2)
        response = c.get(reverse('Preschool_Play:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Preschool_Play/inbox.html')
        self.assertEquals(len(response.context['messages_received']), 0)
        self.assertEquals(len(response.context['messages_sent']), 1)
