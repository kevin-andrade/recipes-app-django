from django.test import TestCase
from django.urls import resolve, reverse

from authors import views


class AuthorViewRegisterTest(TestCase):
    def test_author_view_register_is_correct(self):
        view = resolve(reverse('authors:register'))
        self.assertIs(view.func, views.register)
