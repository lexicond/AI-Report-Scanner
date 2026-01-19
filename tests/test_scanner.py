"""Tests for report scanner"""
import pytest
from datetime import datetime, timedelta
from pathlib import Path
import json
from scanner import ReportScanner
from config import Settings


@pytest.fixture
def mock_settings(tmp_path, monkeypatch):
    """Create mock settings for testing"""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key_123")

    settings = Settings()
    settings.output_dir = tmp_path / "output"
    settings.reports_dir = tmp_path / "reports"
    settings.logs_dir = tmp_path / "logs"
    settings.dry_run = True  # Use dry run to avoid API calls
    settings.create_directories()

    return settings


@pytest.fixture
def scanner(mock_settings):
    """Create scanner instance for testing"""
    return ReportScanner(mock_settings)


class TestReportScanner:
    """Test ReportScanner class"""

    def test_scanner_initialization(self, scanner):
        """Test scanner initializes correctly"""
        assert scanner is not None
        assert scanner.settings is not None
        assert scanner.logger is not None
        assert scanner.seen_reports == set()

    def test_calculate_date_range(self, scanner):
        """Test date range calculation"""
        today, start_date, end_date = scanner._calculate_date_range()

        assert isinstance(today, datetime)
        assert isinstance(start_date, datetime)
        assert isinstance(end_date, datetime)
        assert start_date < end_date
        assert (end_date - start_date).days == scanner.settings.search_days_back

    def test_load_prompt_template(self, scanner, tmp_path):
        """Test loading prompt template"""
        # Create a test prompt file
        test_prompt = "Test prompt with {current_date} and {start_date}"
        prompt_file = Path("search_prompt.txt")

        # Save test prompt
        with open(prompt_file, 'w') as f:
            f.write(test_prompt)

        try:
            loaded = scanner._load_prompt_template()
            assert loaded == test_prompt
        finally:
            # Cleanup not needed as we're using the actual file
            pass

    def test_format_prompt(self, scanner):
        """Test prompt formatting with dates using string replacement"""
        template = "Date: {current_date}, Range: {start_date} to {end_date}, Period: {date_range}, Week: {date}"
        formatted = scanner._format_prompt(
            template,
            "2024-01-15",
            "2024-01-08",
            "2024-01-15"
        )

        assert "2024-01-15" in formatted
        assert "2024-01-08" in formatted
        assert "2024-01-08 to 2024-01-15" in formatted
        # Verify {date} is replaced (used in template)
        assert "{date}" not in formatted
        # Verify other placeholders like {count} for Claude are NOT replaced
        template_with_claude_vars = "Date: {current_date}, Count: {count}"
        formatted2 = scanner._format_prompt(template_with_claude_vars, "2024-01-15", "2024-01-08", "2024-01-15")
        assert "{count}" in formatted2  # Claude's placeholder should remain

    def test_generate_mock_report(self, scanner):
        """Test mock report generation (dry run)"""
        report = scanner._generate_mock_report("2024-01-15")

        assert "reading_list" in report
        assert "notebooklm_source" in report
        assert "metadata" in report
        assert "generated_at" in report
        assert report["generated_at"] == "2024-01-15"
        assert "Mock Report" in report["reading_list"]

    def test_generate_report_dry_run(self, scanner):
        """Test full report generation in dry run mode"""
        report = scanner.generate_report()

        assert report is not None
        assert "reading_list" in report
        assert "notebooklm_source" in report
        assert "metadata" in report
        assert "generated_at" in report

    def test_parse_response_with_notebooklm(self, scanner):
        """Test parsing response with NotebookLM section"""
        class MockContent:
            def __init__(self, text):
                self.type = "text"
                self.text = text

        class MockMessage:
            def __init__(self, text):
                self.content = [MockContent(text)]

        test_text = """# Reading List

Some content here

# NotebookLM Source Document

NotebookLM content here
"""
        message = MockMessage(test_text)
        reading_list, notebooklm = scanner._parse_response(message)

        assert "# Reading List" in reading_list
        assert "# NotebookLM Source Document" in notebooklm
        assert "NotebookLM content" in notebooklm

    def test_parse_response_without_notebooklm(self, scanner):
        """Test parsing response without NotebookLM section"""
        class MockContent:
            def __init__(self, text):
                self.type = "text"
                self.text = text

        class MockMessage:
            def __init__(self, text):
                self.content = [MockContent(text)]

        test_text = "# Reading List\n\nSome content here"
        message = MockMessage(test_text)
        reading_list, notebooklm = scanner._parse_response(message)

        assert "# Reading List" in reading_list
        assert notebooklm == ""

    def test_save_outputs(self, scanner, tmp_path):
        """Test saving outputs to files"""
        report = {
            "reading_list": "# Test Reading List",
            "notebooklm_source": "# Test NotebookLM",
            "metadata": {"model": "test", "tokens": 100},
            "generated_at": "2024-01-15"
        }

        scanner._save_outputs(report)

        # Check files were created
        assert (scanner.settings.reports_dir / "reading_list_2024-01-15.md").exists()
        assert (scanner.settings.reports_dir / "notebooklm_2024-01-15.md").exists()
        assert (scanner.settings.output_dir / "metadata_2024-01-15.json").exists()
        assert (scanner.settings.output_dir / "report_2024-01-15.json").exists()

    def test_validate_report_valid(self, scanner):
        """Test report validation with valid report"""
        valid_report = {
            "reading_list": "# AI & Government Reports\n" + "x" * 200,
            "notebooklm_source": "# NotebookLM Source Document\nContent here",
            "metadata": {
                "model": "claude-sonnet-4",
                "generated_at": "2024-01-15"
            },
            "generated_at": "2024-01-15"
        }

        is_valid, issues = scanner.validate_report(valid_report)
        assert is_valid
        assert len(issues) == 0

    def test_validate_report_missing_keys(self, scanner):
        """Test report validation with missing keys"""
        invalid_report = {
            "reading_list": "Some content"
        }

        is_valid, issues = scanner.validate_report(invalid_report)
        assert not is_valid
        assert len(issues) > 0
        assert any("Missing required key" in issue for issue in issues)

    def test_validate_report_short_content(self, scanner):
        """Test report validation with short content"""
        invalid_report = {
            "reading_list": "Short",
            "notebooklm_source": "# NotebookLM Source Document",
            "metadata": {"model": "test", "generated_at": "2024-01-15"},
            "generated_at": "2024-01-15"
        }

        is_valid, issues = scanner.validate_report(invalid_report)
        assert not is_valid
        assert any("too short" in issue.lower() for issue in issues)

    def test_validate_report_missing_headers(self, scanner):
        """Test report validation with missing headers"""
        invalid_report = {
            "reading_list": "x" * 200,  # Long enough but missing header
            "notebooklm_source": "Content without header",
            "metadata": {"model": "test", "generated_at": "2024-01-15"},
            "generated_at": "2024-01-15"
        }

        is_valid, issues = scanner.validate_report(invalid_report)
        assert not is_valid
        assert any("missing expected header" in issue.lower() for issue in issues)

    def test_seen_reports_tracking(self, scanner, tmp_path):
        """Test tracking of seen reports"""
        # Initially empty
        assert len(scanner.seen_reports) == 0

        # Add some reports
        scanner.seen_reports.add("report1")
        scanner.seen_reports.add("report2")
        scanner._save_seen_reports()

        # Create new scanner instance
        new_scanner = ReportScanner(scanner.settings)

        # Should load previously seen reports
        assert "report1" in new_scanner.seen_reports
        assert "report2" in new_scanner.seen_reports
        assert len(new_scanner.seen_reports) == 2
