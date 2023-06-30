from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views


class RecipeURLsTest(TestCase):
    def test_recipes_url_home_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')
    
    def test_recipes_url_recipe_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'id': 1})
        self.assertEqual(url, '/recipes/1/')

    def test_recipes_url_category_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')


class RecipeViewsTest(TestCase):
    def test_recipes_view_home_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipes_view_recipe_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipes_view_category_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)