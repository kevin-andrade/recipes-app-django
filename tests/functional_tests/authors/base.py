import time
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By

from utils.browser import make_chrome_browser


class AuthorBaseFunctionalTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, qtd=2):
        time.sleep(qtd)

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )
