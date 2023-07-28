from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from django.urls import reverse

from .base import AuthorBaseFunctionalTest


class AuthorLoginFunctionalTest(AuthorBaseFunctionalTest):
    def form_field_login_test_with_callback(self, callback):
        # User open the page login
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # User sees a form, input username e password
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        callback(form, username_field, password_field)
        return form, username_field, password_field

    def test_user_valid_data_can_login_sucessfully(self):
        # Need to create a user
        string_password = '@Password'
        user = User.objects.create_user(
            username='my_user', password=string_password,
        )

        def callback(form, username_field, password_field):

            # User enters his username and password
            username_field.send_keys(user.username)
            password_field.send_keys(string_password)

            # User submits the form
            form.submit()

            self.assertIn(
                'You are logged in with my_user.',
                self.browser.find_element(By.TAG_NAME, 'body').text
            )
        self.form_field_login_test_with_callback(callback)

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create'))

        self.assertIn(
            'Not Found', self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        def callback(form, username_field, password_field):
            # User enters his username and password invalid
            username_field.send_keys(' ')
            password_field.send_keys(' ')

            # User submits the form
            form.submit()

            self.assertIn(
                'Invalid username or password',
                self.browser.find_element(By.TAG_NAME, 'body').text
            )
        self.form_field_login_test_with_callback(callback)

    def test_form_login_invalid_credentials(self):
        def callback(form, username_field, password_field):
            # User enters his username and password invalid credentials
            username_field.send_keys('my_user')
            password_field.send_keys('@password')

            # User submits the form
            form.submit()

            self.assertIn(
                'Invalid credentials',
                self.browser.find_element(By.TAG_NAME, 'body').text
            )
        self.form_field_login_test_with_callback(callback)
