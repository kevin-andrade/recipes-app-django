from unittest.mock import patch
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Sem receitas publicadas no momento 🥲', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_user_search_input_can_find_correct_recipe(self):
        # Need to create a recipe
        recipes = self.make_recipe_in_batch()

        title_needed = "This is what I need"
        recipes[0].title = title_needed
        recipes[0].save()

        # user opens the page
        self.browser.get(self.live_server_url)

        # see a search field named "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Type to search for a recipe"]'
            )

        # click on this input and type the desired title
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # user see what he was looking for
        self.assertIn(
            title_needed,
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        self.sleep(10)
