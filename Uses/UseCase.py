from Resources.PageObjects.Page import Page
from Drivers.Chrome.Config import DriverConfig
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import re
import logging
import time
import datetime
import os


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
            r"^WEBPXTICK_DT-[0-9]+\.zip$",
            r"TickData_structure.dat",
            r"^TC_[0-9]+\.txt$",
            r"TC_structure.dat",
        ]
        self.FAILED_DOWNLOADS = []

    def is_file_downloaded(self, file_name: str, timeout: int = 30) -> bool:
        end_time = time.time() + timeout
        while True:
            for file in os.listdir(DriverConfig.download_directory):
                if re.search(file_name, file):
                    return True

            if time.time() > end_time:
                return False

            time.sleep(1)

    def execute(self, date) -> None:

        # Create log file
        logpath = "./logs_files/"
        log_file_name = (
            f"{logpath}log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        )
        logging.basicConfig(
            filename=log_file_name,
            format="[%(asctime)s] [Line %(lineno)d] [%(levelname)s] %(message)s",
            filemode="w",
            level=logging.INFO,
        )
        log = logging.getLogger("__name__")
        log.setLevel(logging.INFO)

        try:
            if (self.page.does_date_exist(date)) is False:
                raise Exception("No data available for the specified date: {date}")
            for index, data_type in enumerate(self.DATA_TYPES):
                log.info(f"Downloading {data_type} data")
                self.page.select_type_of_data(data_type)
                self.page.select_date(date)
                self.page.download_file()
                time.sleep(0.5)
                if not self.is_file_downloaded(self.EXPECTED_FILES[index]):
                    log.error(f"Failed to download {data_type} data on time")
                    self.FAILED_DOWNLOADS.append(data_type)
                else:
                    log.info(f"SUCCESS: Downloaded {data_type} data")

            if len(os.listdir(DriverConfig.download_directory)) == 4:
                log.info("SUCCESS: All files have been downloaded successfully")
            else:
                # Download Recovery
                for file in self.FAILED_DOWNLOADS:
                    log.info(f"Redownloading {file} data")
                    self.page.select_type_of_data(file)
                    self.page.select_date(date)
                    self.page.download_file()
                    if not self.is_file_downloaded(
                        self.EXPECTED_FILES[self.DATA_TYPES.index(file)]
                    ):
                        log.error(f"Failed to download {data_type} data on time")
                    else:
                        log.info(f"SUCCESS: Downloaded {data_type} data")

        except TimeoutException as e:
            log.error(e)

        except NoSuchElementException as e:
            log.error(e)

        except Exception as e:
            log.error(e)

        finally:
            self.page.driver.quit()
