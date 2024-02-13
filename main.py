from Uses.UseCase import UseCase
from Drivers.Chrome.Config import DriverConfig

import re
import argparse
from datetime import date, datetime
import logging
import os


def setup_logging():
    log_path = "./logs_files/"
    if not os.path.isdir(log_path):
        os.mkdir(log_path)
    logging.basicConfig(
        format="[%(asctime)s] [Line %(lineno)d] [%(levelname)s] %(message)s",
        filemode="w",
        level=logging.INFO,
    )


def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--date",
        type=str,
        help="Specify the date for data retrieval. Use 'Today' for current data, or input in the format: "
        "[Three-letter month abbreviation]-[DD]-[YYYY] (e.g., 'Feb-10-2024').",
    )
    group.add_argument(
        "--number_of_days",
        type=int,
        nargs="?",
        const=-1,
        help="Specify the number of days to retrieve data for. Default is 0, which retrieves all available data.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run the program in headless mode.",
    )
    return parser.parse_args()


def main():
    setup_logging()
    args = parse_arguments()
    download_files = UseCase(DriverConfig(args.headless))

    # if args.number_of_days:
    #     download_files.execute_download_daily_files(args.number_of_days)
    # else:
    #     if args.date.lower() == "today":
    #         download_files.execute_download_all_files(date.today().strftime("%d %b %Y"))
    #     elif re.match(r"[A-Z][a-z]{2}-\d{2}-\d{4}", args.date):
    #         download_files.execute_download_all_files(
    #             datetime.strptime(args.date, "%b-%d-%Y").strftime("%d %b %Y")
    #         )
    #     else:
    #         logging.error("Invalid date format")
    #         exit(1)
    if args.date:
        if args.date.lower() == "today":
            download_files.execute(date=date.today().strftime("%d %b %Y"))
        elif re.match(r"[A-Z][a-z]{2}-\d{2}-\d{4}", args.date):
            download_files.execute(
                date=datetime.strptime(args.date, "%b-%d-%Y").strftime("%d %b %Y")
            )
        else:
            logging.error("Invalid date format")
            exit(1)
    else:
        download_files.execute(number_of_days=args.number_of_days)


if __name__ == "__main__":
    main()
