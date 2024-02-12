from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import datetime
from Uses.UseData import UseData


class DriverConfig:
    if not os.path.isdir(UseData.DOWNLOAD_DIRECTORY):
        os.mkdir(UseData.DOWNLOAD_DIRECTORY)
    __date_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

    service = Service(executable_path=UseData.CHROME_EXECUTABLE_PATH)
    chrome_options = webdriver.ChromeOptions()
    download_directory = os.path.abspath(f"./downloaded_files/{__date_now}_files")
    os.mkdir(download_directory)
    prefs = {"download.default_directory": download_directory}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)

    def get_driver(self):
        return self.driver
