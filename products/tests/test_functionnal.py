from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver

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