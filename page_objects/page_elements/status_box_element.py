from selenium.webdriver.common.by import By


class StatusElement:
    STATUS_USER = (By.CSS_SELECTOR, ".ow_newsfeed_string.ow_small > a")
    STATUS_TEXT = (By.CSS_SELECTOR, ".ow_newsfeed_content")
    STATUS_TIME = (By.CSS_SELECTOR, "a.create_time.ow_newsfeed_date")

    def __init__(self, webelement):
        self.webelement = webelement

    @property
    def text(self):
        return self.webelement.find_element(*self.STATUS_TEXT).text

    @property
    def user(self):
        return self.webelement.find_element(*self.STATUS_USER).text

    @property
    def time(self):
        return self.webelement.find_element(*self.STATUS_TIME).text

    # TODO: Add comments and likes elements.
    # Comments list can be done by using new Comment Element class
