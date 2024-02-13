from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Resources.Locators import Locators
from Uses.UseData import UseData
import logging


class Page:
    """This class contains the methods to interact with the SGX website.

    Attributes:
        driver (webdriver): The instance of the Chrome driver.
        time_and_sales_element (WebElement): The element that contains the time and sales historical data.
    """

    def __init__(self, driver) -> None:
        self.driver = driver
        self.driver.get(UseData.PAGE_URL)
        self.time_and_sales_element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(Locators.TIME_AND_SALES_HISTORICAL_DATA)
        )

    # Method to download the file by clicking the download button
    def download_file(self) -> None:
        self.time_and_sales_element.find_element(*Locators.DOWNLOAD_BUTTON).click()

    # Method to get the elements of the drop down
    def get_dropdown_element(self, by_locator) -> None:
        return self.time_and_sales_element.find_elements(*by_locator)

    # Method to open the drop down
    def open_dropdown(self, dropdown_element) -> None:
        self.driver.implicitly_wait(0.5)
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(dropdown_element)
        )
        dropdown_element.click()

    # Method to select the drop down item
    def select_dropdown_item(self, dropdown_item_locator) -> None:
        select = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(Locators.DROP_DOWN_ITEM_CONTAINER)
        )
        select.find_element(*dropdown_item_locator).click()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(Locators.DROP_DOWN_ITEM_CONTAINER)
        )

    # Method to select the type of data (or file) to download
    def select_type_of_data(self, type_of_data: str) -> None:
        drop_down = self.get_dropdown_element(Locators.DROP_DOWN_TRIGGER)[0]
        self.open_dropdown(drop_down)
        self.select_dropdown_item(Locators.DROP_DOWN_ITEM_SELECT(type_of_data))

    # Method to select the date
    def select_date(self, date: str) -> None:
        drop_down = self.get_dropdown_element(Locators.DROP_DOWN_TRIGGER)[1]
        self.open_dropdown(drop_down)
        self.select_dropdown_item(Locators.DROP_DOWN_ITEM_SELECT(date))

    # Method to check if the date exists in the drop down
    def does_date_exist(self, date: str) -> bool:
        drop_down = self.get_dropdown_element(Locators.DROP_DOWN_TRIGGER)[1]
        self.open_dropdown(drop_down)
        select = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(Locators.DROP_DOWN_ITEM_CONTAINER)
        )
        status = bool(select.find_elements(*Locators.DROP_DOWN_ITEM_SELECT(date)))

        if not status:
            log = logging.getLogger("UseCaseLogger")
            log.error(f"Available data: {select.text.split('\n')}")

        # close the drop down by clicking the trigger again
        self.open_dropdown(drop_down)

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(Locators.DROP_DOWN_ITEM_CONTAINER)
        )

        return status

    def get_available_dates(self) -> list:
        drop_down = self.get_dropdown_element(Locators.DROP_DOWN_TRIGGER)[1]
        self.open_dropdown(drop_down)
        select = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(Locators.DROP_DOWN_ITEM_CONTAINER)
        )
        dates = select.text.split("\n")
        self.open_dropdown(drop_down)
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(Locators.DROP_DOWN_ITEM_CONTAINER)
        )
        return dates
