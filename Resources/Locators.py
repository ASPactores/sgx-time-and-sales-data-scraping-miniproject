from selenium.webdriver.common.by import By


class Locators:
    """This class contains the locators for the SGX website.

    Attributes:
        TIME_AND_SALES_HISTORICAL_DATA (tuple): The locator for the element that contains the time and sales historical
        data.
        DOWNLOAD_BUTTON (tuple): The locator for the download button.
        DROP_DOWN_TRIGGER (tuple): The locator for the drop down trigger.
        DROP_DOWN_ITEM_CONTAINER (tuple): The locator for the drop down item container.

    Method:
        DROP_DOWN_ITEM_SELECT(title: str) -> tuple: Locator Generator for the individual drop down items.
    """

    TIME_AND_SALES_HISTORICAL_DATA = (
        By.TAG_NAME,
        "widget-reports-derivatives-tick-and-trade-cancellation",
    )
    DOWNLOAD_BUTTON = (By.TAG_NAME, "button")
    DROP_DOWN_TRIGGER = (By.TAG_NAME, "input")
    DROP_DOWN_ITEM_CONTAINER = (By.TAG_NAME, "sgx-list")

    def DROP_DOWN_ITEM_SELECT(title: str) -> tuple:
        return (
            By.XPATH,
            f"//sgx-select-picker-option[@title='{title}']",
        )
