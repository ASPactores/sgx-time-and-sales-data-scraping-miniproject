import os


class UseData:
    """This class contains the data used by the application.

    Attributes:
        CHROME_EXECUTABLE_PATH (str): The path to the Chrome driver executable.
        PAGE_URL (str): The URL of the SGX website.
        DOWNLOAD_DIRECTORY (str): The path to the directory where the downloaded files will be saved.
        ABSOLUTE_DOWNLOAD_DIRECTORY (str): The absolute path to the download directory.
    """

    CHROME_EXECUTABLE_PATH = os.path.abspath("Drivers/Chrome/chromedriver.exe")
    PAGE_URL = "https://www.sgx.com/research-education/derivatives"
    DOWNLOAD_DIRECTORY = "./downloaded_files"
    ABSOLUTE_DOWNLOAD_DIRECTORY = os.path.abspath(DOWNLOAD_DIRECTORY)
