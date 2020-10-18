from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True


class FirefoxFunctionalTestCases(StaticLiveServerTestCase):
    """Functional tests using the Firefox web browser in headless mode."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox(firefox_options=firefox_options)
        cls.driver.implicitly_wait(30)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.driver.quit()

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(
            username="jeanpierre", password="password24!"
        )

    def test_user_can_connect_and_disconnect(self):

        self.driver.get(self.live_server_url)
        self.driver.find_element_by_css_selector('#login').click()
        self.driver.find_element_by_css_selector('#id_username').send_keys(
            "jeanpierre"
        )
        self.driver.find_element_by_css_selector('#id_password').send_keys(
            "password54!"
        )
        self.driver.find_element_by_css_selector('#button-submit').click()

        self.assertTemplateUsed('home.html')

    def test_reset_password(self):

        self.driver.get(self.live_server_url)
        self.driver.find_element_by_css_selector('#login').click()
        self.driver.find_element_by_css_selector('#id_username').send_keys(
            "jeanpierre"
        )
        self.driver.find_element_by_css_selector('#id_password').send_keys(
            "password24!"
        )
        self.driver.find_element_by_css_selector('#button-submit').click()
        self.driver.find_element_by_css_selector('#reset').click()
        self.driver.find_element_by_css_selector('#id_email').send_keys(
            "jeanpierre@gmail.com"
        )
        self.assertTemplateUsed('password_reset_done.html')

    def test_export(self):

        self.driver.get(self.live_server_url)
        self.driver.find_element_by_css_selector('#login').click()
        self.driver.find_element_by_css_selector('#id_username').send_keys(
            "jeanpierre"
        )
        self.driver.find_element_by_css_selector('#id_password').send_keys(
            "password24!"
        )
        self.driver.find_element_by_css_selector('#button-submit').click()
        self.driver.find_element_by_css_selector('#export').click()

    def test_autocomplete(self):

        self.driver.get(self.live_server_url)
        self.driver.find_element_by_css_selector('#product').send_keys(
            "nute"
        )
        self.driver.find_element_by_css_selector('#product').send_keys(Keys.ARROW_DOWN)
        self.driver.find_element_by_css_selector('#product').click()
        self.driver.find_element_by_css_selector('#button_design').click()
        self.assertTemplateUsed('result.html')