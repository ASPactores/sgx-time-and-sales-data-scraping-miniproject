# sgx-scraping-miniproject

### Prerequisite

- Google Chrome Version **121.0.6167.161**
- Pipenv (can be installed using `pip install pipenv`)
- Python version 3.12

### Project implementation details

This program is a utility designed to retrieve specific files from the [SGX website](https://www.sgx.com/research-education/derivatives) based on user-defined dates. The program downloads the following files:

- WEBPXTICK_DT-\*.zip
- TickData_structure.dat
- TC\_\*.txt
- TC_structure.dat

These files will be saved to the directory `./downloaded_files/{datetime}`. A log file will also be generated to record the program's activities. The log file will be saved to the directory `./logs_files/log_{datetime}.log`.

In the event of a download failure, the program is equipped to automatically retry fetching the missing files up to **three times**.

## Running the program

### Running the virtual environment:

- Run `pipenv install` or `python -m pipenv install` to install the dependencies
- Run `pipenv shell` or `python -m pipenv shell` to spin up a virtual environment

### Command line options:

| Option            | Description                                                                                                                                                                                        |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--date [string]` | Facilitates the selection of download dates. Follows the format: `[Three-letter Month Abbreviation]-[DD]-[YYYY]`. Alternatively, users can also use `Today` to download data for the current date. |
| `--headless`      | Runs the web scraper in headless mode.                                                                                                                                                             |

### Example usage:

- `python main.py --date Today --headless`
- `python main.py --date Feb-08-2024`
