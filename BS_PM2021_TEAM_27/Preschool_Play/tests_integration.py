import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.utils import override_settings
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from .models import *
import os
# from pyvirtualdisplay import Display


class TestIntegrationWithSelenium(StaticLiveServerTestCase):

    def setUp(self):
        driver = './win-geckodriver.exe'
        opts = FirefoxOptions()
        if os.name != 'nt':
            driver = './geckodriver-linux64'
            opts.add_argument("--headless")
            # display = Display(visible=0, size=(800, 600))
            # display.start()
        self.browser = webdriver.Firefox(executable_path=driver, firefox_options=opts)

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
        self.user = User.objects.create_user(username='parent')
        self.user.set_password('qwerty246')
        self.user.save()
        self.profile = UserProfile(user=self.user, type='parent')
        self.profile.save()
        self.kid = Child(name='kid2', parent=self.profile, teacher=self.teacher_profile, kindergarten=self.kg,
                         auth=True, suspension_time=datetime.now() + timedelta(hours=1))
        self.kid.save()

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
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        self.browser.find_element_by_xpath('//a[text()="Add Child"]').click()
        time.sleep(1)
        child_name = self.browser.find_element_by_name("name_child")
        child_name.send_keys('kid1')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        self.browser.find_element_by_xpath('//a[text()="Delete Child"]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//select/option[text()="Name: kid1. Parent: user1"]').click()
        pass_kid = self.browser.find_element_by_name("password")
        pass_kid.send_keys('qwerty246')
        self.browser.find_element_by_xpath('//input[@type="submit"]').click()

    def test_add_child_and_approve_this_child_from_user_of_his_teacher(self):
        self.browser.get(f'{self.live_server_url}/preschoolplay/login')
        username_input = self.browser.find_element_by_name("user_name")
        username_input.send_keys('parent')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('qwerty246')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        self.browser.find_element_by_xpath('//a[text()="Add Child"]').click()
        time.sleep(1)
        child_name = self.browser.find_element_by_name("name_child")
        child_name.send_keys('kid1')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        self.browser.find_element_by_xpath('//a[text()="Logout"]').click()
        self.browser.get(f'{self.live_server_url}/preschoolplay/login')
        username_input = self.browser.find_element_by_name("user_name")
        username_input.send_keys('teacher1')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('qwerty246')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        self.browser.switch_to.alert.accept()
        time.sleep(1)
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        self.browser.find_element_by_xpath('//a[text()="Approve Student"]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//a[text()="kid1"]').click()
        self.browser.find_element_by_xpath("//a[@href='/preschoolplay/final-approve/kid1']").click()

    def test_suspend_child_and_make_sure_he_is_on_his_teachers_suspended_list(self):
        self.browser.get(f'{self.live_server_url}/preschoolplay/login')
        username_input = self.browser.find_element_by_name("user_name")
        username_input.send_keys('parent')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('qwerty246')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        self.browser.find_element_by_xpath('//a[text()="My Children"]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath("//h5[@class='card-title' and text()='kid2']")
        time.sleep(1)
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        self.browser.find_element_by_xpath('//a[text()="Logout"]').click()
        self.browser.get(f'{self.live_server_url}/preschoolplay/login')
        username_input = self.browser.find_element_by_name("user_name")
        username_input.send_keys('teacher1')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('qwerty246')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        self.browser.find_element_by_xpath('//a[text()="Child Suspension"]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath("//div[contains(., 'kid2')]")
        time.sleep(1)

    def test_sending_and_receiving_messages_between_two_users(self):
        def wait_page_load():
            time.sleep(0.5)

        self.browser.get(f'{self.live_server_url}/preschoolplay/login')
        username_input = self.browser.find_element_by_name("user_name")
        username_input.send_keys('user1')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('qwerty246')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        wait_page_load()
        self.browser.get(f'{self.live_server_url}/preschoolplay')
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        wait_page_load()
        self.browser.find_element_by_xpath('//a[text()="Inbox"]').click()
        wait_page_load()
        self.browser.find_element_by_xpath('//a[text()="Send new message"]').click()
        wait_page_load()
        self.browser.find_element_by_xpath('//select[@name="receiver"]/option[text()="admin"]').click()
        wait_page_load()
        subject_input = self.browser.find_element_by_name("subject")
        subject_input.send_keys('this new app')
        subject_input = self.browser.find_element_by_name("body")
        subject_input.send_keys('random text')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        self.browser.get(f'{self.live_server_url}/preschoolplay')
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        wait_page_load()
        self.browser.find_element_by_xpath('//a[text()="Logout"]').click()
        wait_page_load()
        self.browser.get(f'{self.live_server_url}/preschoolplay/login')
        username_input = self.browser.find_element_by_name("user_name")
        username_input.send_keys('admin')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('qwerty246')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        wait_page_load()
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        wait_page_load()
        self.browser.find_element_by_xpath('//a[text()="Inbox(1)"]').click()
        wait_page_load()
        self.browser.find_element_by_xpath('//a[text()=" Open"]').click()
        message_subject = self.browser.find_element_by_xpath('//h3')
        self.assertEquals('this new app' in message_subject.text, True)

    def test_register_as_teacher_and_add_kindergarten_and_parent_register_his_child_to_this_kindergarten(self):
        self.browser.get(f'{self.live_server_url}/preschoolplay/new-user')
        register_input = self.browser.find_element_by_name("username")
        register_input.send_keys('teacher2')
        password_input = self.browser.find_element_by_name("password1")
        password_input.send_keys('qwerty246')
        password_input = self.browser.find_element_by_name("password2")
        password_input.send_keys('qwerty246')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        address_input = self.browser.find_element_by_name("address")
        address_input.send_keys('address')
        self.browser.find_element_by_xpath('//select/option[text()="teacher"]').click()
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        self.browser.get(f'{self.live_server_url}/preschoolplay/login')
        username_input = self.browser.find_element_by_name("user_name")
        username_input.send_keys('teacher2')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('qwerty246')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        self.browser.find_element_by_xpath('//a[text()="Create Kindergarten"]').click()
        time.sleep(1)
        kn_input = self.browser.find_element_by_name("name")
        kn_input.send_keys('kindergartenNew')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        self.browser.find_element_by_xpath('//a[text()="Logout"]').click()
        self.browser.get(f'{self.live_server_url}/preschoolplay/login')
        username_input = self.browser.find_element_by_name("user_name")
        username_input.send_keys('parent')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('qwerty246')
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//a[text()="Main Menu"]').click()
        self.browser.find_element_by_xpath('//a[text()="Add Child"]').click()
        time.sleep(1)
        child_name = self.browser.find_element_by_name("name_child")
        child_name.send_keys('kid1')
        self.browser.find_element_by_xpath('//select/option[text()="teacher2"]').click()
        self.browser.find_element_by_xpath('//select/option[text()="kindergartenNew"]').click()
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(1)