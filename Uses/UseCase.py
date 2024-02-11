from Resources.PageObjects.Page import Page
from Drivers.Chrome.Config import DriverConfig

# from Uses.UseData import UseData

# import os
import re


import time


class UseCase:
    def __init__(self) -> None:
        self.page = Page(DriverConfig.driver)
        self.page.driver.maximize_window()
        self.page.driver.execute_script("window.scrollTo(0, 233)")
        self.DATA_TYPES = [
            "Tick",
            "Tick Data Structure",
            "Trade Cancellation",
            "Trade Cancellation Data Structure",
        ]
        self.EXPECTED_FILES = [
            r"WEBPXTICK_DT-.+\.zip",
            r"TickData_structure\.dat",
            r"TC_.+\.txt",
            r"TC_structure\.dat",
        ]
        self.FAILED_DOWNLOADS = []

    # TODO: fix this because it may produce a bug when previous file has already been downloaded
    def is_file_downloaded(self, file_name: str, timeout: int = 5) -> bool:
        end_time = time.time() + timeout
        while True:
            for pattern in self.EXPECTED_FILES:
                if re.match(pattern, file_name):
                    return True

            if time.time() > end_time:
                return False

            time.sleep(1)

    def execute(self) -> None:
        date = "07 Feb 2024"
        if (self.page.does_date_exist(date)) is False:
            # Throw Exception
            print(f"Date: {date} does not exist")

            self.page.driver.quit()
            return
        for index, data_type in enumerate(self.DATA_TYPES):
            self.page.select_type_of_data(data_type)
            self.page.select_date(date)
            self.page.download_file()
            time.sleep(0.5)
            if not self.is_file_downloaded(self.EXPECTED_FILES[index]):
                self.FAILED_DOWNLOADS.append(data_type)

        self.page.driver.quit()
