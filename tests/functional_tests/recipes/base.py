from django.test import LiveServerTestCase
import time

from recipes.tests.test_recipe_base import RecipeMixin
from utils.browser import make_chrome_browser


class RecipeBaseFunctionalTest(LiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=2):
        time.sleep(seconds)
