import os


class UseData:
    CHROME_EXECUTABLE_PATH = os.path.abspath("Drivers/Chrome/chromedriver.exe")
    PAGE_URL = "https://www.sgx.com/research-education/derivatives"
    DOWNLOAD_DIRECTORY = "./downloaded_files"
    ABSOLUTE_DOWNLOAD_DIRECTORY = os.path.abspath(DOWNLOAD_DIRECTORY)
