import pytest
import sys

from main import combine_multiple_reports, run
from report import ClickbaitReport


@pytest.fixture
def sample_report():
    return "title,ctr,retention_rate\nVideo1,25,10\nVideo2,5,80\nVideo3,30,12"


def test_cli(sample_report, tmp_path, monkeypatch, capsys):
    test_file = tmp_path / "test.csv"
    test_file.write_text(sample_report)

    monkeypatch.setattr(sys, 'argv', [
        'main.py',
        '--files', str(test_file),
        '--report', 'clickbait'
    ])
    run()

    captured = capsys.readouterr()
    assert "Video1" in captured.out
    assert "25" in captured.out
    assert "Video2" not in captured.out


def test_wrong_path():
    with pytest.raises(FileNotFoundError):
        combine_multiple_reports([''])


def test_wrong_report_name(sample_report, tmp_path, monkeypatch):
    test_file = tmp_path / "test.csv"
    test_file.write_text(sample_report)

    monkeypatch.setattr(sys, 'argv', [
        'main.py',
        '--files', str(test_file),
        '--report', ''
    ])

    run()

    assert pytest.raises(KeyError)


def test_get_clickbait_report_filtering(sample_report, tmp_path):
    file = tmp_path / 'test.csv'
    file.write_text(sample_report)

    report = ClickbaitReport(combine_multiple_reports([file]))
    result = report.get_report()

    assert len(result) ==2
    assert result[0]['title'] == 'Video3' and result[1]['title'] == 'Video1'


def test_get_clickbait_report_sorting(sample_report, tmp_path):
    file = tmp_path / 'test.csv'
    file.write_text(sample_report)

    report = ClickbaitReport(combine_multiple_reports([file]))
    result = report.get_report()

    assert result[0]['title'] == 'Video3'
    assert float(result[0]['ctr']) > float(result[1]['ctr'])


def test_combine_multiple_reports_single_report(tmp_path):
    file_1 = tmp_path / 'test1.csv'
    file_1.write_text('title,ctr,retention_rate\n'
                      'Video1,20,30')

    result = combine_multiple_reports([str(file_1)])
    assert len(result) == 1
    assert result[0]['title'] == 'Video1'


def test_combine_multiple_reports(tmp_path):
    test_file_1 = tmp_path / 'test1.csv'
    test_file_1.write_text('title,ctr,retention_rate\n'
                           'Video1,20,30')
    test_file_2 = tmp_path / 'test2.csv'
    test_file_2.write_text('title,ctr,retention_rate\n'
                           'Video2,25,20')
    test_file_3 = tmp_path / 'test3.csv'
    test_file_3.write_text('title,ctr,retention_rate\n'
                           'Video3,17,15\n'
                           'Video4,41,21')

    result = combine_multiple_reports([str(test_file_1), str(test_file_2), str(test_file_3)])
    assert len(result) == 4
    assert result[0]['title'] == 'Video1'
