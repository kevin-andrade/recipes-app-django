from django.urls import resolve, reverse
from recipes import views
from .test_recipes_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipes_view_home_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipes_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipes_home_views_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipes_home_template_shows_no_recipe_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>Sem receitas publicadas no momento 🥲</h1>',
            response.content.decode('utf-8')
        )
    
    def test_recipes_home_template_loads_recipes(self):
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

    def test_recipes_view_recipe_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertIs(view.func, views.recipe)

    def test_recipes_view_recipe_returns_404_if_no_recipes(self):
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipes_view_category_is_correct(self):
        view = resolve(reverse(
            'recipes:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipes_view_category_returns_404_if_no_recipes(self):
        response = self.client.get(reverse(
            'recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

