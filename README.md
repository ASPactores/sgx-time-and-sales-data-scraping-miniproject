# sgx-scraping-miniproject

### Prerequisite

- Google Chrome Version <u>**121.0.6167.161**</u>
- Pipenv (can be installed using `pip install pipenv`)

### Project implementation details

This program is a utility designed to retrieve specific files from the [SGX website](https://www.sgx.com/research-education/derivatives) based on user-defined dates. The program downloads the following files:

- WEBPXTICK_DT-\*.zip
- TickData_structure.dat
- TC\_\*.txt
- TC_structure.dat

In the event of a download failure, the program is equipped to automatically retry fetching the missing files up to **_three times_**.

## Running the program

### Command Line Options:

    | Command | Description |
    | :------ | :---------- |

args:
--document-date [string] "Feb-20-2024" or "Today"
