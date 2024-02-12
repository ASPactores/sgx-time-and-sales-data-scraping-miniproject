from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import datetime
from Uses.UseData import UseData


class DriverConfig:
    """This class contains the configuration for the Chrome driver."""

    if not os.path.isdir(UseData.ABSOLUTE_DOWNLOAD_DIRECTORY):
        os.mkdir(UseData.ABSOLUTE_DOWNLOAD_DIRECTORY)

    _date_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    download_directory = os.path.abspath(
        f"{UseData.DOWNLOAD_DIRECTORY}/{_date_now}_files"
    )
    if not os.path.isdir(download_directory):
        os.mkdir(download_directory)

    _service = Service(executable_path=UseData.CHROME_EXECUTABLE_PATH)
    _chrome_options = webdriver.ChromeOptions()
    _prefs = {"download.default_directory": download_directory}
    _chrome_options.add_experimental_option("prefs", _prefs)

    driver = webdriver.Chrome(options=_chrome_options)
