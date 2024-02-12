from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import datetime
from Uses.UseData import UseData


class DriverConfig:
    """This class contains the configuration for the Chrome driver."""

    def __init__(self, headless=False) -> None:
        if not os.path.isdir(UseData.ABSOLUTE_DOWNLOAD_DIRECTORY):
            os.mkdir(UseData.ABSOLUTE_DOWNLOAD_DIRECTORY)

        self._date_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        self.download_directory = os.path.abspath(
            f"{UseData.DOWNLOAD_DIRECTORY}/{self._date_now}_files"
        )
        if not os.path.isdir(self.download_directory):
            os.mkdir(self.download_directory)

        self._service = Service(executable_path=UseData.CHROME_EXECUTABLE_PATH)
        self._chrome_options = webdriver.ChromeOptions()
        self._prefs = {"download.default_directory": self.download_directory}
        self._chrome_options.add_experimental_option("prefs", self._prefs)

        if headless:
            self._chrome_options.add_argument("--headless")
            userAgent = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/84.0.4147.56 Safari/537.36"
            )
            self._chrome_options.add_argument(f"user-agent={userAgent}")

        self.driver = webdriver.Chrome(options=self._chrome_options)
