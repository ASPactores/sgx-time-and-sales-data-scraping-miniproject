from Uses.UseCase import UseCase

import re
import argparse
from datetime import date, datetime
import logging
import os


if __name__ == "__main__":
    download_files = UseCase()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        type=str,
        default="Today",
        help="Specify the date for data retrieval. Use 'Today' for current data, or input in the format: "
        "[Three-letter month abbreviation]-[DD]-[YYY] (e.g., 'Feb-10-2024').",
    )

    args = parser.parse_args()

    # Create log path
    logPath = "./logs_files/"
    if not (os.path.isdir(logPath)):
        os.mkdir(logPath)

    logging.basicConfig(
        format="[%(asctime)s] [Line %(lineno)d] [%(levelname)s] %(message)s",
        filemode="w",
        level=logging.INFO,
    )

    if args.date.lower() == "today":
        download_files.execute(date.today().strftime("%d %b %Y"))
    elif re.match(r"[A-Z][a-z]{2}-\d{2}-\d{4}", args.date):
        download_files.execute(
            datetime.strptime(args.date, "%b-%d-%Y").strftime("%d %b %Y")
        )
    else:
        logging.error("Invalid date format")
        exit(1)
