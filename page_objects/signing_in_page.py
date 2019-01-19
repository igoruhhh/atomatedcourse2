from selenium.webdriver.support.expected_conditions import invisibility_of_element_located

from page_objects.dashboard_page import DashboardPage
from page_objects.page import Page
from locators.locator import SignInLocators
from page_objects.page_elements.input_text_field import InputTextElement


class SignInPage(Page):
    # def __init__(self, driver):
    #     super().__init__(driver)
    #     self.username_field = self.find_visible_element(locator.LOGIN_FIELD)
    #  Not good decision, because we can get staleness elements over time

    @property
    def username_field(self):
        return InputTextElement(self.find_visible_element(SignInLocators.LOGIN_FIELD))

    @property
    def password_field(self):
        return InputTextElement(self.find_visible_element(SignInLocators.PASS_FIELD))

    @property
    def sign_in_button(self):
        return self.find_visible_element(SignInLocators.SIGN_IN_BUTTON)

    def is_this_page(self):
        return self.is_element_present(SignInLocators.LOGIN_WINDOW_BOX)

    def submit_form(self):
        self.sign_in_button.click()
        self.wait.until(invisibility_of_element_located(SignInLocators.LOGIN_BACKGROUND),
                        "Login background is still visible")
        # return DashboardPage(self.driver)


if __name__ == "__main__":
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1/oxwall")
    from page_objects.main_page import MainPage
    main_page = MainPage(driver)
    main_page.sign_in_menu.click()

    sign_in_page = SignInPage(driver)
    # 1st type of using:
    sign_in_page.username_field.input("something")
    sign_in_page.password_field.input("some_pass")
    sign_in_page.submit_form()
