"""Integration tests for the complete workflow"""
import pytest
from pathlib import Path
import json
from config import Settings
from scanner import ReportScanner
from notifications import NotificationService


@pytest.fixture
def integration_settings(tmp_path, monkeypatch):
    """Settings for integration testing"""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key_integration")
    monkeypatch.setenv("SENDER_EMAIL", "sender@example.com")
    monkeypatch.setenv("RECIPIENT_EMAIL", "recipient@example.com")
    monkeypatch.setenv("EMAIL_PASSWORD", "test_password")

    settings = Settings()
    settings.output_dir = tmp_path / "output"
    settings.reports_dir = tmp_path / "reports"
    settings.logs_dir = tmp_path / "logs"
    settings.dry_run = True  # Use dry run for integration tests
    settings.create_directories()

    return settings


class TestIntegration:
    """Integration tests for complete workflow"""

    def test_full_workflow_dry_run(self, integration_settings):
        """Test complete workflow in dry run mode"""
        # Initialize scanner
        scanner = ReportScanner(integration_settings)

        # Generate report
        report = scanner.generate_report()

        # Validate report structure
        assert "reading_list" in report
        assert "notebooklm_source" in report
        assert "metadata" in report
        assert "generated_at" in report

        # Validate report content
        is_valid, issues = scanner.validate_report(report)
        assert is_valid, f"Report validation failed: {issues}"

        # Check files were created
        generated_date = report['generated_at']
        assert (integration_settings.reports_dir / f"reading_list_{generated_date}.md").exists()
        assert (integration_settings.reports_dir / f"notebooklm_{generated_date}.md").exists()
        assert (integration_settings.output_dir / f"metadata_{generated_date}.json").exists()

    def test_output_file_contents(self, integration_settings):
        """Test that output files contain expected content"""
        scanner = ReportScanner(integration_settings)
        report = scanner.generate_report()

        generated_date = report['generated_at']

        # Check reading list file
        reading_list_file = integration_settings.reports_dir / f"reading_list_{generated_date}.md"
        content = reading_list_file.read_text()
        assert "# AI & Government Reports" in content
        assert "## 🔥 CRITICAL" in content

        # Check NotebookLM file
        notebooklm_file = integration_settings.reports_dir / f"notebooklm_{generated_date}.md"
        content = notebooklm_file.read_text()
        assert "# NotebookLM Source Document" in content

        # Check metadata file
        metadata_file = integration_settings.output_dir / f"metadata_{generated_date}.json"
        metadata = json.loads(metadata_file.read_text())
        assert "model" in metadata
        assert "generated_at" in metadata

    def test_logging_output(self, integration_settings):
        """Test that logging works correctly"""
        scanner = ReportScanner(integration_settings)
        scanner.generate_report()

        # Check that log file was created
        log_files = list(integration_settings.logs_dir.glob("scanner_*.log"))
        assert len(log_files) > 0

        # Check log file contains expected content
        log_content = log_files[0].read_text()
        assert "Starting weekly report generation" in log_content
        assert "Report generation completed" in log_content or "DRY RUN MODE" in log_content

    def test_seen_reports_persistence(self, integration_settings):
        """Test that seen reports are persisted across runs"""
        # First run
        scanner1 = ReportScanner(integration_settings)
        scanner1.seen_reports.add("test_report_1")
        scanner1.seen_reports.add("test_report_2")
        scanner1._save_seen_reports()

        # Second run - new scanner instance
        scanner2 = ReportScanner(integration_settings)

        # Should load previously seen reports
        assert "test_report_1" in scanner2.seen_reports
        assert "test_report_2" in scanner2.seen_reports

    def test_multiple_runs_different_dates(self, integration_settings, monkeypatch):
        """Test multiple runs create separate output files"""
        scanner = ReportScanner(integration_settings)

        # First run
        report1 = scanner.generate_report()
        date1 = report1['generated_at']

        # Simulate different date for second run
        from datetime import datetime, timedelta
        original_calculate = scanner._calculate_date_range

        def mock_calculate():
            today = datetime.now() + timedelta(days=1)
            start = today - timedelta(days=7)
            return today, start, today

        scanner._calculate_date_range = mock_calculate

        # Second run
        report2 = scanner.generate_report()
        date2 = report2['generated_at']

        # Should have different dates
        assert date1 != date2

        # Both sets of files should exist
        assert (integration_settings.reports_dir / f"reading_list_{date1}.md").exists()
        assert (integration_settings.reports_dir / f"reading_list_{date2}.md").exists()

    def test_error_handling_missing_prompt(self, integration_settings):
        """Test error handling when prompt template is missing"""
        # Temporarily move prompt file
        prompt_file = Path("search_prompt.txt")
        backup_file = Path("search_prompt.txt.backup")

        if prompt_file.exists():
            prompt_file.rename(backup_file)

        try:
            scanner = ReportScanner(integration_settings)

            with pytest.raises(FileNotFoundError):
                scanner.generate_report()

        finally:
            # Restore prompt file
            if backup_file.exists():
                backup_file.rename(prompt_file)

    def test_notification_service_integration(self, integration_settings):
        """Test notification service with generated report"""
        scanner = ReportScanner(integration_settings)
        report = scanner.generate_report()

        notification_service = NotificationService(integration_settings)

        # Test that notification methods can be called without errors
        # (they will fail due to invalid credentials, but shouldn't crash)
        text = notification_service._format_email_text(report)
        assert text is not None
        assert report['generated_at'] in text

        html = notification_service._format_email_html(report)
        assert html is not None
        assert report['generated_at'] in html

    def test_directory_creation_on_init(self, tmp_path, monkeypatch):
        """Test that necessary directories are created on initialization"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key")

        base_path = tmp_path / "test_scanner"
        settings = Settings()
        settings.output_dir = base_path / "output"
        settings.reports_dir = base_path / "reports"
        settings.logs_dir = base_path / "logs"

        # Directories should not exist yet
        assert not settings.output_dir.exists()

        # Create directories
        settings.create_directories()

        # Initialize scanner (should not fail even though directories didn't exist)
        scanner = ReportScanner(settings)
        assert scanner is not None

        # Directories should be created
        assert settings.output_dir.exists()
        assert settings.reports_dir.exists()
        assert settings.logs_dir.exists()
