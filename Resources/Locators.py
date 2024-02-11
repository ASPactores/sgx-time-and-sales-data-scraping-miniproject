from selenium.webdriver.common.by import By


class Locators:
    TIME_AND_SALES_HISTORICAL_DATA = (
        By.TAG_NAME,
        "widget-reports-derivatives-tick-and-trade-cancellation",
    )
    DOWNLOAD_BUTTON = (By.TAG_NAME, "button")
    DROP_DOWN_TRIGGER = (By.TAG_NAME, "input")
    DROP_DOWN_ITEM_CONTAINER = (By.TAG_NAME, "sgx-list")

    # --- Drop Down Item ---
    # Locator Generator for the individual drop down items
    def DROP_DOWN_ITEM_SELECT(title: str) -> tuple:
        return (
            By.XPATH,
            f"//sgx-select-picker-option[@title='{title}']",
        )

    # Type of Data Drop Down Item
    ITEM_TICK = DROP_DOWN_ITEM_SELECT("Tick")
    ITEM_TICK_DATA_STRUCTURE = DROP_DOWN_ITEM_SELECT("Tick Data Structure")
    ITEM_TRADE_CANCELLATION = DROP_DOWN_ITEM_SELECT("Trade Cancellation")
    TRADE_CANCELLATION_DATA_STRUCTURE = DROP_DOWN_ITEM_SELECT(
        "Trade Cancellation Data Structure"
    )
