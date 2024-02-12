from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Resources.Locators import Locators
from Uses.UseData import UseData


class Page:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.driver.get(UseData.PAGE_URL)
        self.time_and_sales_element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(Locators.TIME_AND_SALES_HISTORICAL_DATA)
        )

    def download_file(self) -> None:
        self.time_and_sales_element.find_element(*Locators.DOWNLOAD_BUTTON).click()

    def get_dropdown_element(self, by_locator) -> None:
        return self.time_and_sales_element.find_elements(*by_locator)

    def open_dropdown(self, dropdown_element) -> None:
        self.driver.implicitly_wait(0.5)
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(dropdown_element)
        )
        dropdown_element.click()

    def select_dropdown_item(self, dropdown_item_locator) -> None:
        select = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(Locators.DROP_DOWN_ITEM_CONTAINER)
        )
        select.find_element(*dropdown_item_locator).click()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(Locators.DROP_DOWN_ITEM_CONTAINER)
        )

    def select_type_of_data(self, type_of_data: str) -> None:
        drop_down = self.get_dropdown_element(Locators.DROP_DOWN_TRIGGER)[0]
        self.open_dropdown(drop_down)
        self.select_dropdown_item(Locators.DROP_DOWN_ITEM_SELECT(type_of_data))

    def select_date(self, date: str) -> None:
        drop_down = self.get_dropdown_element(Locators.DROP_DOWN_TRIGGER)[1]
        self.open_dropdown(drop_down)
        self.select_dropdown_item(Locators.DROP_DOWN_ITEM_SELECT(date))

    def does_date_exist(self, date: str) -> bool:
        drop_down = self.get_dropdown_element(Locators.DROP_DOWN_TRIGGER)[1]
        self.open_dropdown(drop_down)
        select = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(Locators.DROP_DOWN_ITEM_CONTAINER)
        )

        return bool(select.find_elements(*Locators.DROP_DOWN_ITEM_SELECT(date)))
