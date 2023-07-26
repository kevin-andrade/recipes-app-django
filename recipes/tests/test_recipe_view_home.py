from django.urls import resolve, reverse
from unittest.mock import patch
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewHomeTest(RecipeTestBase):
    def test_recipe_view_home_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_views_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipe_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>Sem receitas publicadas no momento 🥲</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        '''Test recipe is published False'''
        # Need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        # Check if one recipe exists if not show message
        self.assertIn(
            '<h1>Sem receitas publicadas no momento 🥲</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn('Recipe Title', content)
        # self.assertIn('10 Minutos', content)
        # self.assertIn('5 Porções', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_view_is_paginated(self):
        # Need more recipe to increase the pages
        for i in range(20):
            kwargs = {'author_data': {'username': f'us{i}'}, 'slug': f'sl{i}'}
            self.make_recipe(**kwargs)

        # patch used to modify per_page variable without changing
        with patch('recipes.views.PER_PAGE', new=9):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            # search for number of pages and size of content displayed per page
            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 9)
            self.assertEqual(len(paginator.get_page(2)), 9)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=12A')
            self.assertEqual(
                response.context['recipes'].number,
                1
            )
            response = self.client.get(reverse('recipes:home') + '?page=2')
            self.assertEqual(
                response.context['recipes'].number,
                2
            )
            response = self.client.get(reverse('recipes:home') + '?page=3')
            self.assertEqual(
                response.context['recipes'].number,
                3
            )
