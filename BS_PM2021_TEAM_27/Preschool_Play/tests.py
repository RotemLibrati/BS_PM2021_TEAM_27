from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, Client, tag
from django.test.utils import override_settings
from django.urls import reverse, resolve
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from . import views
from .models import *


# py manage.py test
# Create your tests here.


class TestInboxView(TestCase):
    def test_without_login(self):
        c = Client()
        response = c.get(reverse('Preschool_Play:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Not logged in")

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


class TestViewMessage(TestCase):
    def test_message_content(self):
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
        response = c.get(reverse('Preschool_Play:view-message', args=[message.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Preschool_Play/message.html')
        self.assertContains(response, 'hello')

    # def test_message_does_not_exist(self):
    #     c = Client()
    #     user = User.objects.create_user(username='tester1', password='qwerty246')
    #     user.save()
    #     user_profile = UserProfile.objects.create(user=user)
    #     user_profile.save()
    #     c.force_login(user)
    #     response = c.get(reverse('Preschool_Play:view-message', args=[3]))
    #     self.assertEqual(response.status_code, 200)
    # self.assertTemplateUsed(response, 'Preschool_Play/error.html')
    # self.assertContains(response, 'Message getting failed')


class TestNewMessage(TestCase):
    def test_new_message_template_content(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        c.force_login(user)
        response = c.get(reverse('Preschool_Play:new-message'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Preschool_Play/new-message.html')
        self.assertContains(response, 'New message')

    def test_message_post(self):
        c = Client()
        user = User.objects.create_user(username='tester1', password='qwerty246')
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        user2 = User.objects.create_user(username='tester2', password='qwerty246')
        user2.save()
        user_profile2 = UserProfile.objects.create(user=user2)
        user_profile2.save()
        message = {'receiver': user, 'subject': 'subject', 'body': 'body'}
        c.force_login(user2)
        response = c.post(reverse('Preschool_Play:new-message'), data=message)
        self.assertRedirects(response, reverse('Preschool_Play:inbox'))
        m = Message.objects.get(receiver=user, sender=user2)
        self.assertIsNotNone(m)


@tag('unit-test')
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


class TestScoreGraphsView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.user.set_password('Qwerty246')
        self.user.save()

    def test_admin_access(self):
        self.profile = UserProfile(user=self.user, is_admin=True)
        self.profile.save()
        self.client = Client()
        self.client.login(username='testuser', password='Qwerty246')
        response = self.client.get(reverse('Preschool_Play:scoregraphs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Daily sum")
        self.assertTemplateUsed(response, 'Preschool_Play/score-graphs.html')

    def test_unauthorized_access(self):
        self.profile = UserProfile(user=self.user, is_admin=False)
        self.profile.save()
        self.client = Client()
        self.client.login(username='testuser', password='Qwerty246')
        response = self.client.get(reverse('Preschool_Play:scoregraphs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unauthorized user")
        self.assertTemplateUsed(response, 'Preschool_Play/error.html')

    def test_parent_access(self):
        self.profile = UserProfile(user=self.user, is_admin=False)
        self.profile.save()
        self.child = Child(name='son', parent=self.profile)
        self.child.save()
        self.client = Client()
        self.client.login(username='testuser', password='Qwerty246')
        response = self.client.get(reverse('Preschool_Play:scoregraphs', kwargs={'name': 'son'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Daily sum")
        self.assertTemplateUsed(response, 'Preschool_Play/score-graphs.html')

    def test_teacher_access(self):
        self.profile = UserProfile(user=self.user, type='parent')
        self.profile.save()
        self.teacher = User.objects.create(username='teacher_user')
        self.teacher.set_password('Qwerty246')
        self.teacher.save()
        self.teacher_profile = UserProfile(user=self.teacher, type='teacher')
        self.teacher_profile.save()
        self.child = Child(name='ben', parent=self.profile, teacher=self.teacher_profile)
        self.child.save()
        self.score_date = datetime.now()
        self.score = Score(child=self.child, amount=22, date=self.score_date)
        self.score.save()
        self.client = Client()
        self.client.login(username='teacher_user', password='Qwerty246')
        response = self.client.get(reverse('Preschool_Play:scoregraphs', kwargs={'name': 'ben'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ben")
        self.assertTemplateUsed(response, 'Preschool_Play/score-graphs.html')


@tag('unit-test')
class TestSuspensionView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.user.set_password('Qwerty246')
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


@tag('unit-test')
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


class TestParentView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Qwerty246')
        self.user.save()
        self.profile = UserProfile(user=self.user, type='parent')
        self.profile.save()
        self.child = Child(name='son', parent=self.user.profile)
        self.child.save()

    def test_child_is_visible_in_parent_page(self):
        self.client = Client()
        self.client.login(username='testuser', password='Qwerty246')
        response = self.client.get(reverse('Preschool_Play:parent'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "son")
        self.assertTemplateUsed(response, 'Preschool_Play/parent.html')


class TestMyStudentsView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Qwerty246')
        self.user.save()
        self.profile = UserProfile(user=self.user, type='parent')
        self.profile.save()
        self.teacher = User.objects.create_user(username='teacher_user', password='Qwerty246')
        self.user.save()
        self.teacher_profile = UserProfile(user=self.teacher, type='teacher')
        self.teacher_profile.save()
        self.child = Child(name='ben', parent=self.profile, teacher=self.teacher_profile)
        self.child.save()
        self.score_date = datetime.now()
        self.score = Score(child=self.child, amount=22, date=self.score_date)

    def test_with_teacher_login(self):
        self.client = Client()
        self.client.login(username='teacher_user', password='Qwerty246')
        response = self.client.get(reverse('Preschool_Play:my-students'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ben")
        self.assertTemplateUsed(response, 'Preschool_Play/my-students.html')


# @tag('unit-test')
# class TestMediaView(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='Qwerty246')
#         self.user.save()
#         self.profile = UserProfile(user=self.user, is_admin=True)
#         self.profile.save()
#         self.client = Client()
#         self.client.login(username='testuser', password='Qwerty246')
#
#     def test_with_add_media(self):
#         response = self.client.get(reverse('Preschool_Play:add-media'))
#         self.assertEqual(response.status_code, 200)
#         add_media = Media(name='name', path='www/rrr/ttt', type='picture')
#         add_media.save()
#         self.assertContains(response, "Add Media")
#
#     def test_with_delete_media(self):
#         response = self.client.get(reverse('Preschool_Play:delete-media'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Delete Media")
class TestMediaView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.user.set_password('Qwerty246')
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


@tag('unit-test')
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
    # def test_Preschool_Play_add_media_url_is_resolved(self):
    #     url = reverse('Preschool_Play:add-media')
    #     self.assertEqual(resolve(url).func, views.add_media)
    #
    # def test_Preschool_Play_delete_media_url_is_resolved(self):
    #     url = reverse('Preschool_Play:delete-media')
    #     self.assertEqual(resolve(url).func, views.delete_media)


@tag('unit-test')
class TestMessageBoardView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.user.set_password('Qwerty246')
        self.user.save()
        self.profile = UserProfile(user=self.user, is_admin=False)
        self.profile.save()

    def test_message_creation(self):
        mes = Message(sender=self.user, subject='hi', is_public=True)
        mes.save()
        self.client = Client()
        self.client.login(username='testuser', password='Qwerty246')
        response = self.client.get(reverse('Preschool_Play:message-board'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hi")
        self.assertContains(response, "testuser")
        self.assertTemplateUsed(response, 'Preschool_Play/message-board.html')


class TestNewMessageView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.user.set_password('Qwerty246')
        self.user.save()
        self.profile = UserProfile(user=self.user, type='parent')
        self.profile.save()
        self.teacher_user = User.objects.create_user(username='teacher1', password='Qwerty246')
        self.teacher_user.save()
        self.teacher_profile = UserProfile(user=self.teacher_user, type='teacher')
        self.teacher_profile.save()
        self.child = Child(name='ben', parent=self.user.profile, teacher=self.teacher_profile)
        self.child.save()
        self.client = Client()
        self.client.login(username='testuser', password='Qwerty246')

    # def test_teacher_of_child_shows_up_in_new_message_page(self):
    #     response = self.client.get(reverse('Preschool_Play:new-message'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "teacher1")
    #     self.assertTemplateUsed(response, 'Preschool_Play/new-message.html')


class TestIntegrationWithSelenium(StaticLiveServerTestCase):

    def setUp(self):
        firefox_binary = FirefoxBinary('./')
        self.browser = webdriver.Firefox(firefox_binary=firefox_binary)

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
        self.user = User.objects.create_user(username='user1')
        self.user.set_password('qwerty246')
        self.user.save()
        self.profile = UserProfile(user=self.user, is_admin=True)
        self.profile.save()

    def tearDown(self):
        self.browser.close()

    @override_settings(DEBUG=True)
    def test_login_then_add_and_delete_new_child(self):
        self.browser.get(f'{self.live_server_url}/preschoolplay/login')
        username_input = self.browser.find_element_by_name("user_name")
        username_input.send_keys('user1')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('qwerty246')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        self.browser.find_element_by_xpath('//a[text()="Add Child"]').click()
        child_name = self.browser.find_element_by_name("name_child")
        child_name.send_keys('kid1')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        self.browser.find_element_by_xpath('//a[text()="Delete Child"]').click()
        self.browser.find_element_by_xpath('//select/option[text()="Name: kid1. Parent: user1"]').click()
        self.browser.find_element_by_xpath('//input[@type="submit"]').click()

    def test_sending_and_receiving_messages_between_two_users(self):
        self.browser.get(f'{self.live_server_url}/preschoolplay/login')
        username_input = self.browser.find_element_by_name("user_name")
        username_input.send_keys('user1')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('qwerty246')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        self.browser.get(f'{self.live_server_url}/preschoolplay')
        self.browser.find_element_by_xpath('//a[text()="Inbox"]').click()
        self.browser.find_element_by_xpath('//a[text()="Send new message"]').click()
        self.browser.find_element_by_xpath('//select[@name="receiver"]/option[text()="admin"]').click()
        subject_input = self.browser.find_element_by_name("subject")
        subject_input.send_keys('this new app')
        subject_input = self.browser.find_element_by_name("body")
        subject_input.send_keys('random text')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        self.browser.get(f'{self.live_server_url}/preschoolplay')
        self.browser.find_element_by_xpath('//a[text()="Logout"]').click()
        self.browser.get(f'{self.live_server_url}/preschoolplay/login')
        username_input = self.browser.find_element_by_name("user_name")
        username_input.send_keys('admin')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('qwerty246')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        self.browser.find_element_by_xpath('//a[text()="Inbox(1)"]').click()
        self.browser.find_element_by_xpath('//a[text()=" Open"]').click()
        message_subject = self.browser.find_element_by_xpath('//h3')
        self.assertEquals('this new app' in message_subject.text, True)
