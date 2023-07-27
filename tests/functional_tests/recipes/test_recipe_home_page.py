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

        title_needed = "This is the recipe I want"
        recipes[0].title = title_needed
        recipes[0].save()

        # user opens the page
        self.browser.get(self.live_server_url)

        # see a search field named "Type to search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Type to search for a recipe"]'
        )

        # click on this input and type the desired title
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        self.sleep(5)

        # user see what he was looking for
        self.assertIn(
            title_needed, 
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_home_page_pagination(self):
        # Create a recipe
        self.make_recipe_in_batch()

        # User open the page
        self.browser.get(self.live_server_url)

        # User see that it has pagination and click on the second page
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # User see there are 2 more recipes on page 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 2
        )

        self.sleep(8)
