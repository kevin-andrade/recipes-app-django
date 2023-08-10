from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewSearchTest(RecipeTestBase):
    def test_recipe_view_search_uses_correct_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func.view_class, views.RecipeListSearch)

    def test_recipe_search_views_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=test')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_scaped(self):
        url = reverse('recipes:search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is title one'
        title2 = 'This is title two'

        recipe1 = self.make_recipe(
            title=title1, slug='one', author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            title=title2, slug='two', author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    def test_recipe_search_can_find_recipe_by_description(self):
        description1 = 'This is desc one'
        description2 = 'This is desc two'

        recipe1 = self.make_recipe(
            slug='one',
            description=description1,
            author_data={'username': 'one'},
        )
        recipe2 = self.make_recipe(
            slug='two',
            description=description2,
            author_data={'username': 'two'},
        )

        search_url = reverse('recipes:search')
        response_desc_1 = self.client.get(f'{search_url}?q={description1}')
        response_desc_2 = self.client.get(f'{search_url}?q={description2}')
        response_both_description = self.client.get(f'{search_url}?q=desc')

        self.assertIn(recipe1, response_desc_1.context['recipes'])
        self.assertNotIn(recipe2, response_desc_1.context['recipes'])

        self.assertIn(recipe2, response_desc_2.context['recipes'])
        self.assertNotIn(recipe1, response_desc_2.context['recipes'])

        self.assertIn(recipe1, response_both_description.context['recipes'])
        self.assertIn(recipe2, response_both_description.context['recipes'])
