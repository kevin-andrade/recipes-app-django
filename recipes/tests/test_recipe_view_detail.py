from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewDetailTest(RecipeTestBase):
    def test_recipe_view_detail_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1000}))
        self.assertIs(view.func.view_class, views.RecipeDetail)

    def test_recipe_view_detail_returns_404_if_no_recipes(self):
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'pk': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_views_loads_correct_template(self):
        # Need recipe.id for this test
        recipe = self.make_recipe()
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'pk': recipe.id}))
        self.assertTemplateUsed(response, 'recipes/pages/recipe-view.html')

    def test_recipe_detail_template_loads_correct_recipe(self):
        # Need a recipe for this test
        needed_title = 'This is a title recipe - It load a one recipe'
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'pk': 1}
        ))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)
        self.assertIn('10 Minutos', content)
        # self.assertIotted names into their objects. ..n('5 Porções', content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        '''Test recipe is published False'''
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'pk': recipe.id}
        ))

        # Check if one recipe is not published
        self.assertEqual(response.status_code, 404)
