from Resources.PageObjects.Page import Page
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import re
import logging
import time
import datetime
import os


class FileManager:
    """Class to check if the expected files have been downloaded.

    Attributes:
        expected_files (list): A list of regular expressions to match the names of the expected files.

    Method:
        is_file_downloaded(file_name: str, timeout: int) -> bool:
            Check if the file has been downloaded within the specified timeout period.
    """

    def __init__(self, expected_files, driver_config):
        self.expected_files = expected_files
        self.driver_config = driver_config

    def is_file_downloaded(self, file_name: str, timeout: int = 30) -> bool:
        end_time = time.time() + timeout
        while True:
            for file in os.listdir(self.driver_config.download_directory):
                if re.search(file_name, file):
                    return True
            if time.time() > end_time:
                return False
            time.sleep(1)


class UseCase:
    """Class to handle the use case of downloading data from the SGX website.

    Attributes:
        page (Page): An instance of the Page class to interact
            with the SGX website.
        driver_config (DriverConfig): An instance of the DriverConfig class to configure the Chrome driver.
        DATA_TYPES (list): A list of data types to download.
        EXPECTED_FILES (list): A list of regular expressions to match the names of the expected files.
        FAILED_DOWNLOADS (list): A list to store the data types that failed to download.
        file_manager (FileManager): An instance of the FileManager class to check if the expected files have been
            downloaded.
    """

    def __init__(self, driver_config):
        self.page = Page(driver_config.driver)
        self.page.driver.maximize_window()
        self.page.driver.execute_script("window.scrollTo(0, 233)")
        self.driver_config = driver_config
        self.DATA_TYPES = [
            "Tick",
            "Tick Data Structure",
            "Trade Cancellation",
            "Trade Cancellation Data Structure",
        ]
        self.EXPECTED_FILES = [
            r"^WEBPXTICK_DT-[0-9]+\.zip$",
            r"TickData_structure.dat",
            r"^TC_[0-9]+\.txt$",
            r"TC_structure.dat",
        ]
        self.FAILED_DOWNLOADS = []
        self.file_manager = FileManager(self.EXPECTED_FILES, driver_config)

    # Execute the use case to download data for the specified date.
    def execute(self, date) -> None:
        log = self._initialize_logger()
        try:
            log.info(f"Starting data download for date: {date}")
            if not self.page.does_date_exist(date):
                raise Exception(f"No data available for the specified date: {date}")
            for index, data_type in enumerate(self.DATA_TYPES):
                self._download_data(data_type, date, index, log)
            self._handle_download_recovery(date, log)
        except (TimeoutException, NoSuchElementException, Exception) as e:
            log.error(e)
        finally:
            log.info("Finished process.")
            self.page.driver.quit()

    # Initialize the logger for the use case.
    def _initialize_logger(self):
        logpath = "./logs_files/"
        log_file_name = (
            f"{logpath}log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        )
        log = logging.getLogger()
        log_handler = logging.FileHandler(filename=log_file_name, mode="w")
        log_handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [Line %(lineno)d] [%(levelname)s] %(message)s"
            )
        )
        log.addHandler(log_handler)
        log.setLevel(logging.INFO)

        return log

    # Download the specified data type for the given date.
    def _download_data(self, data_type, date, index, log):
        log.info(f"Downloading {data_type} data")
        self.page.select_type_of_data(data_type)
        self.page.select_date(date)
        time.sleep(0.5)
        self.page.download_file()
        if not self.file_manager.is_file_downloaded(self.EXPECTED_FILES[index]):
            log.error(f"Failed to download {data_type} data on time")
            self.FAILED_DOWNLOADS.append(data_type)
        else:
            log.info(f"SUCCESS: Downloaded {data_type} data")

    # Handle the recovery of failed downloads by redownloading the files up to a maximum number of three (3) retries.
    def _handle_download_recovery(self, date, log, maxRetry=3):
        if len(os.listdir(self.driver_config.download_directory)) == 4:
            log.info("SUCCESS: All files have been downloaded successfully")
        else:
            retries = 0
            while retries < maxRetry:
                log.info(
                    f"Attempting to redownload failed files. [Attempt {retries + 1}]"
                )
                for file in self.FAILED_DOWNLOADS.copy():
                    log.info(f"Redownloading {file} data")
                    self.page.select_type_of_data(file)
                    self.page.select_date(date)
                    self.page.download_file()
                    if not self.file_manager.is_file_downloaded(
                        self.EXPECTED_FILES[self.DATA_TYPES.index(file)]
                    ):
                        log.error(f"Failed to download {file} data on time")
                    else:
                        log.info(f"SUCCESS: Downloaded {file} data")
                        self.FAILED_DOWNLOADS.remove(file)
                if len(self.FAILED_DOWNLOADS) == 0:
                    log.info("SUCCESS: All files have been downloaded successfully")
                    break
                elif retries == maxRetry - 1:
                    log.error(
                        f"Failed to download the following files: {self.FAILED_DOWNLOADS}"
                    )
                retries += 1
