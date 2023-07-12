from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewCategoryTest(RecipeTestBase):
    def test_recipe_view_category_is_correct(self):
        view = resolve(reverse(
            'recipes:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_view_category_returns_404_if_no_recipes(self):
        response = self.client.get(reverse(
            'recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_correct_recipe(self):
        # Need a recipe for this test
        needed_title = 'This is a title recipe'
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse(
            'recipes:category', kwargs={'category_id': 1}
        ))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipe_not_published(self):
        '''Test recipe is published False'''
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse(
            'recipes:category', kwargs={'category_id': recipe.category.id}
        ))

        # Check if one recipe is not published
        self.assertEqual(response.status_code, 404)

    # def test_recipe_category_view_is_paginated(self):
    #     # Need more recipe to increase the pages
    #     category_test = self.make_category()
    #     for i in range(6):
    #         kwargs = {
    #             'author_data': {'username': f'us{i}'},
    #             'slug': f'sl{i}'
    #             }
    #         self.make_recipe_with_same_category(
    #             category_data=category_test, **kwargs)

    #     # patch used to modify per_page variable without changing
    #     with patch('recipes.views.PER_PAGE', new=2):
    #         response = self.client.get(
    #             reverse('recipes:category',
    #                     kwargs={'category_id': 1}))
    #         recipes = response.context['recipes']
    #         paginator = recipes.paginator

    #         # search for number of pages and size of content displayed per page
    #         self.assertEqual(paginator.num_pages, 3)
    #         self.assertEqual(len(paginator.get_page(1)), 2)
    #         self.assertEqual(len(paginator.get_page(2)), 2)
    #         self.assertEqual(len(paginator.get_page(3)), 2)
