from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from Uses.UseData import UseData


class DriverConfig:
    service = Service(executable_path=UseData.CHROME_EXECUTABLE_PATH)
    chrome_options = webdriver.ChromeOptions()
    download_directory = UseData.DOWNLOAD_DIRECTORY
    prefs = {"download.default_directory": download_directory}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)

    def get_driver(self):
        return self.driver
