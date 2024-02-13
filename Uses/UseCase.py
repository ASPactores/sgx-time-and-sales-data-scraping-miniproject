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
        self.log = self._initialize_logger()

    # Main method to execute the use case.
    def execute(self, date=None, number_of_days=None):
        try:
            if date:
                self._execute_download_all_files(date)
            elif number_of_days:
                self._execute_download_daily_files(number_of_days)
            else:
                raise Exception(
                    "Invalid arguments. Please specify either a date or a number of days."
                )
        except (TimeoutException, NoSuchElementException, Exception) as e:
            self.log.error(e)
        finally:
            self.log.info("Finished process.")
            self.page.driver.quit()

    # Execute the use case to download data for the specified date.
    def _execute_download_all_files(self, date) -> None:
        self.log.info(f"Starting data download for date: {date}")
        if not self.page.does_date_exist(date):
            raise Exception(f"No data available for the specified date: {date}")

        # Create a new directory to organize downloaded data by date.
        new_directory = f"{self.driver_config.download_relative_directory}/{date}"
        absolute_new_directory = os.path.abspath(new_directory)
        if not os.path.isdir(absolute_new_directory):
            os.mkdir(absolute_new_directory)

        for index, data_type in enumerate(self.DATA_TYPES):
            self._download_data(data_type, date, index)
            filename = self._find_file(self.EXPECTED_FILES[index])
            os.rename(
                os.path.join(self.driver_config.download_directory, filename),
                os.path.abspath(f"{new_directory}/{filename}"),
            )
        self._handle_download_recovery(date, directory=absolute_new_directory)

    # Download data for the specified number of days.
    def _execute_download_daily_files(self, number_of_days=-1) -> None:
        dates = self.page.get_available_dates()
        if len(dates) == 0:
            raise Exception("No data available.")
        if number_of_days == -1:
            number_of_days = len(dates)
        elif number_of_days > len(dates):
            self.log.info(
                "Requested no. of dates exceeds available dates. "
                f"There are only {len(dates)} dates. "
                "Downloading available data."
            )
            number_of_days = len(dates)
        for date in dates[:number_of_days]:
            self._execute_download_all_files(date)

    # Find the file in the download directory that matches the specified pattern.
    def _find_file(self, pattern):
        files = os.listdir(self.driver_config.download_directory)

        matched_files = [file for file in files if re.match(pattern, file)]

        if not matched_files:
            return -1

        return matched_files[0]

    # Initialize the logger for the use case.
    def _initialize_logger(self):
        logpath = "./logs_files/"
        log_file_name = (
            f"{logpath}log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        )
        log = logging.getLogger("UseCaseLogger")
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
    def _download_data(self, data_type, date, index):
        self.log.info(f"Downloading {data_type} data")
        self.page.select_type_of_data(data_type)
        self.page.select_date(date)
        time.sleep(0.5)
        self.page.download_file()
        if not self.file_manager.is_file_downloaded(self.EXPECTED_FILES[index]):
            self.log.error(f"Failed to download {data_type} data from date: {date}")
            self.FAILED_DOWNLOADS.append(data_type)
        else:
            self.log.info(f"SUCCESS: Downloaded {data_type} data from date: {date}")

    # Handle the recovery of failed downloads by redownloading the files up to a maximum number of three (3) retries.
    def _handle_download_recovery(self, date, maxRetry=3, directory=None):
        if directory is None:
            directory = self.driver_config.download_directory

        if len(os.listdir(directory)) == 4:
            self.log.info(
                f"SUCCESS: All files for {date} have been downloaded successfully"
            )
        else:
            retries = 0
            while retries < maxRetry:
                self.log.info(
                    f"Attempting to redownload failed files. [Attempt {retries.__add__(1)}]"
                )
                for file in self.FAILED_DOWNLOADS.copy():
                    self.log.info(f"Redownloading {file} data")
                    self.page.select_type_of_data(file)
                    self.page.select_date(date)
                    self.page.download_file()
                    if not self.file_manager.is_file_downloaded(
                        self.EXPECTED_FILES[self.DATA_TYPES.index(file)]
                    ):
                        self.log.error(f"Failed to download {file} data on time")
                    else:
                        self.log.info(f"SUCCESS: Downloaded {file} data")
                        self.FAILED_DOWNLOADS.remove(file)
                if len(self.FAILED_DOWNLOADS) == 0:
                    self.log.info(
                        f"SUCCESS: All files for {date} have been downloaded successfully"
                    )
                    break
                elif retries == maxRetry - 1:
                    self.log.error(
                        f"Failed to download the following files: {self.FAILED_DOWNLOADS}"
                    )
                retries.__add__(1)
