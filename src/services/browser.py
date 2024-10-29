from app import SELENIUM_HOST_URL
from src.constants import SELENIUM_BROWSER_DIMENSIONS


class ChromeBrowser:
    def __init__(
        self,
        driver=None,
        remote=False,
        remote_url=SELENIUM_HOST_URL,
        dimensions=SELENIUM_BROWSER_DIMENSIONS,
    ):
        self.driver = driver
        self.remote = remote
        self.remote_url = remote_url
        self.browser_width = dimensions[0]
        self.browser_height = dimensions[1]

    def setup_driver(self):
        from selenium import webdriver

        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--browserTimeout=3")
        options.add_argument("--headless")
        options.add_experimental_option("detach", True)
        if self.remote:
            self.driver = webdriver.Remote(
                command_executor=self.remote_url,
                options=options,
            )
        self.driver.set_window_size(self.browser_width, self.browser_height)
        return self.driver

    def teardown_driver(self):
        self.driver.quit()

    def test_visit_site(self):
        self.driver.get("http://localhost:5000/")
        assert "OK" in self.driver.page_source
