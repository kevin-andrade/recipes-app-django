from .base import AuthorBaseFunctionalTest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AuthorRegisterFunctionalTest(AuthorBaseFunctionalTest):
    # def test_the_test(self):
    #     self.browser.get(self.live_server_url + '/authors/register/')
    #     self.sleep()

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(
            By.TAG_NAME,
            'input'
        )

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 6)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        # Open the authors register page
        self.browser.get(self.live_server_url + '/authors/register')

        # Select all form
        form = self.get_form()

        # Fill in the fields with dummy data
        # Need to create a valid email
        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('test@test.com')

        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            # Look for the first name field and the field error
            first_name_field = self.get_by_placeholder(form, "Ex.: Keven")
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)

            # Need to resend to see the message
            form = self.get_form()

            self.sleep()
            # Assert the message error
            self.assertIn('Write your first name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            # Look for the first name field and the field error
            last_name_field = self.get_by_placeholder(form, "Ex.: Andrade")
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            # Need to resend to see the message
            form = self.get_form()

            self.sleep()
            # Assert the message error
            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            # Look for the first name field and the field error
            username_field = self.get_by_placeholder(form, "Your username")
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            # Need to resend to see the message
            form = self.get_form()

            self.sleep()
            # Assert the message error
            self.assertIn('This field is required', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            # Look for the first name field and the field error
            email_field = self.get_by_placeholder(form, "Your e-mail")
            email_field.send_keys('test@test.')
            email_field.send_keys(Keys.ENTER)

            # Need to resend to see the message
            form = self.get_form()

            self.sleep()
            # Assert the message error
            self.assertIn('The e-mail must be valid', form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match_error_message(self):
        def callback(form):
            # Look for the first name field and the field error
            password1_field = self.get_by_placeholder(form, "Type your password")
            password2_field = self.get_by_placeholder(form, "Repeat your password")

            password1_field.send_keys('@Password1')
            password2_field.send_keys('@Password1_different')
            password2_field.send_keys(Keys.ENTER)

            # Need to resend to see the message
            form = self.get_form()

            self.sleep()
            # Assert the message error
            self.assertIn('Password must be equal', form.text)
        self.form_field_test_with_callback(callback)
