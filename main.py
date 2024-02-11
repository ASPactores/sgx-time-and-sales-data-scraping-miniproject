# import scraper.open as scraper

from Uses.UseCase import UseCase

if __name__ == "__main__":
    # scraper
    download_files = UseCase()
    download_files.execute()
