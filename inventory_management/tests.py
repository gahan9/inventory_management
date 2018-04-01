# coding=utf-8
import os
import time
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse_lazy

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from inventory_management.utils import pickler


class LoginTestSelenium(StaticLiveServerTestCase):
    def setUp(self):
        self.credentials = {
            "username": "root",
            "password": "r@123456"
        }
        User.objects.create(username=self.credentials['username'],
                            password=make_password(self.credentials['password']))

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # settings.DEBUG = True
        # driver = webdriver.Chrome(r"F:\dev\_selenium\ChromeDriver\chromedriver.exe")
        cls.selenium = webdriver.Chrome(getattr(settings, "CHROME_DRIVER_PATH", r"F:\dev\_selenium\ChromeDriver\chromedriver.exe"))
        cls.selenium.implicitly_wait(15)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('{}{}'.format(self.live_server_url, reverse_lazy('login')))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(self.credentials['username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(self.credentials['password'])
        self.selenium.find_element_by_id('login').click()
        time.sleep(5)


class GTPLlogin(LiveServerTestCase):
    def setUp(self):
        self.login_url = "http://www.gtpl.net/login/login.php"
        self.register_ticket_url = "http://www.gtpl.net/login/register_ticket.php"
        _path = os.path.join(getattr(settings, 'MEDIA_ROOT'), "credentials.pickle")
        self.credentials = pickler(1, path=_path)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # settings.DEBUG = True
        cls.selenium = webdriver.Chrome(getattr(settings, "CHROME_DRIVER_PATH", r"F:\dev\_selenium\ChromeDriver\chromedriver.exe"))
        cls.selenium.implicitly_wait(15)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(self.login_url)
        username_input = self.selenium.find_element_by_name("txtuname")
        username_input.send_keys(self.credentials['username'])  # Enter username
        password_input = self.selenium.find_element_by_name("txtpwd")
        password_input.send_keys(self.credentials['password'])  # Enter password
        self.selenium.execute_script("$('#radio1').click()")  # Select Broadband
        self.selenium.find_element_by_name('submit').click()  # login
        time.sleep(5)  # sleep.. (awaits seconds before closing browser)

    def test_register_ticket(self):
        self.selenium.get(self.register_ticket_url)
        time.sleep(30)
