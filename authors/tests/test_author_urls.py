from django.test import TestCase
from django.urls import reverse


class AuthorURLsTest(TestCase):
    def test_recipe_url_home_is_correct(self):
        url = reverse('authors:register')
        self.assertEqual(url, '/authors/register/')
