import argparse
import csv

from tabulate import tabulate


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
            print(f'LOG: processed file #{index + 1}: {file_path}')
    return combined_report


def get_clickbait_report(report: list[dict]) -> list[dict]:
    """
    Only keeps TITLE, CTR>15% and RETENTION_RATE<40% columns.
    Returns the report that meets needed requirements
    """
    print('LOG: report type: CLICKBAIT(title, ctr>15%, retention_rate<40%)')

    retention_rate_percentage_max = 40
    ctr_percentage_min = 15
    keep_cols = ['title', 'ctr', 'retention_rate']

    final_report = []
    for row in report:
        filtered_row = {col: row[col] for col in keep_cols}
        if float(filtered_row['ctr']) > ctr_percentage_min and float(
                filtered_row['retention_rate']) < retention_rate_percentage_max:
            final_report.append(filtered_row)

    return sorted(final_report, key=lambda sort_row: float(sort_row['ctr']), reverse=True)

REPORT_TYPES = {
    'clickbait': get_clickbait_report,
}

def run():
    parser = argparse.ArgumentParser(
        prog='YouTube metrics reader')
    parser.add_argument('-f', '--files', nargs='+', help='CSV report files paths')
    parser.add_argument('-r', '--report', type=str, help='report table name')

    args = parser.parse_args()
    file_paths = args.files
    report_name = args.report

    try:
        raw_combined_report = combine_multiple_reports(file_paths)  # first we combine the reports to not mess up sorting
        try:
            final_report = REPORT_TYPES[report_name](raw_combined_report)
            if final_report:
                print(tabulate(final_report, headers='keys', tablefmt='grid'))
            else:
                print('ERROR: could not generate a report')
        except KeyError:
            print('ERROR: there is no such REPORT TYPE')
    except FileNotFoundError:
        print('ERROR: could not find ONE OF or ALL the files listed')


if __name__ == '__main__':
    run()
