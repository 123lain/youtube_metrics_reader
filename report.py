import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class Report(ABC):
    def __init__(self, report):
        self.report = report

    @abstractmethod
    def get_report(self):
        """Returns the report that meets needed requirements"""
        pass


class ClickbaitReport(Report):
     def get_report(self) -> list[dict]:
        """
        Only keeps TITLE, CTR>15% and RETENTION_RATE<40% columns.
        Returns the report that meets needed requirements
        """
        logger.info('report type: CLICKBAIT(title, ctr>15%, retention_rate<40%)')

        retention_rate_percentage_max = 40
        ctr_percentage_min = 15
        keep_cols = ['title', 'ctr', 'retention_rate']

        final_report = []
        for row in self.report:
            filtered_row = {col: row[col] for col in keep_cols}
            if float(filtered_row['ctr']) > ctr_percentage_min and float(
                    filtered_row['retention_rate']) < retention_rate_percentage_max:
                final_report.append(filtered_row)

        return sorted(final_report, key=lambda sort_row: float(sort_row['ctr']), reverse=True)


REPORT_TYPES = {
    'clickbait': ClickbaitReport,
}