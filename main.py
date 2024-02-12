from Uses.UseCase import UseCase
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
    parser.add_argument(
        "--date",
        type=str,
        default="Today",
        help="Specify the date for data retrieval. Use 'Today' for current data, or input in the format: "
        "[Three-letter month abbreviation]-[DD]-[YYYY] (e.g., 'Feb-10-2024').",
    )
    return parser.parse_args()


def main():
    setup_logging()
    args = parse_arguments()
    download_files = UseCase()

    if args.date.lower() == "today":
        download_files.execute(date.today().strftime("%d %b %Y"))
    elif re.match(r"[A-Z][a-z]{2}-\d{2}-\d{4}", args.date):
        download_files.execute(
            datetime.strptime(args.date, "%b-%d-%Y").strftime("%d %b %Y")
        )
    else:
        logging.error("Invalid date format")
        exit(1)


if __name__ == "__main__":
    main()
