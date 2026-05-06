import argparse
import csv
import logging
from tabulate import tabulate
from report import ClickbaitReport, REPORT_TYPES
from ctr_logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)


def combine_multiple_reports(file_paths: list[str]) -> list[dict]:
    """
    Takes a list of csv file paths and combines them into a single report
    """
    combined_report = []
    for index, file_path in enumerate(file_paths):
        with open(file_path, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)  # using DictReader instead of reader helps to deal with headers easier
            for row in reader:
                combined_report.append(row)
            logger.info(f'processed file #{index + 1}: {file_path}')
    return combined_report


def run():
    parser = argparse.ArgumentParser(
        prog='YouTube metrics reader')
    parser.add_argument('-f', '--files', nargs='+', help='CSV report files paths')
    parser.add_argument('-r', '--report', type=str, help='report table name')

    args = parser.parse_args()
    file_paths = args.files
    report_name = args.report

    try:
        report = REPORT_TYPES[report_name](combine_multiple_reports(file_paths))  # first we combine the reports to not mess up sorting
        final_report = ClickbaitReport.get_report(report)
        if final_report:
            print(tabulate(final_report, headers='keys', tablefmt='grid'))
        else:
            logger.error('could not generate a report')
    except FileNotFoundError:
        logger.error('could not find ONE OF or ALL the files listed')
    except KeyError:
        logger.error('there is no such REPORT TYPE')


if __name__ == '__main__':
    run()
