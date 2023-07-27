from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from authors.forms import RegisterForm
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex.: Keven'),
        ('last_name', 'Ex.: Andrade'),
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', (
            'Username must have letters, numbers or one of those @.+-_.'
            'The length should be between 4 and 150 characters.'
        )),
        ('email', 'The e-mail must be valid.'),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.')),
    ])
    def test_fields_help_text_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'first_name': 'first',
            'last_name': 'last',
            'username': 'user',
            'email': 'email@anyemail.com',
            'password': 'Strong@Password1',
            'password2': 'Strong@Password2',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field is required'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'E-mail is required'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_min_length_should_be_4(self):
        self.form_data['username'] = 'Kev'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have at least 4 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_max_length_should_be_150(self):
        self.form_data['username'] = 'K' * 151

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have less than 150 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_password_field_is_correct(self):
        self.form_data['password'] = 'Abc1234@'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password2_confirmation_are_equal(self):
        self.form_data['password'] = 'Abc1234@'
        self.form_data['password2'] = 'Abc1234@'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Password must be equal'
        self.assertNotIn(msg, response.content.decode('utf-8'))

        # Not equal
        self.form_data['password'] = 'Abc1234@'
        self.form_data['password2'] = 'Abc12345@'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_register_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_field_email_must_be_unique(self):
        url = reverse('authors:register_create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'E-mail already in use'
        email_errors = response.context['form'].errors.get('email')

        if email_errors is not None:
            self.assertIn(msg, email_errors)
            self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_register_created_can_login(self):
        url = reverse('authors:register_create')

        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc12345',
            'password2': '@Bc12345',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='@Bc12345',
        )

        self.assertTrue(is_authenticated)
