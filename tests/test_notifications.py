"""Tests for notification system"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from notifications import NotificationService
from config import Settings


@pytest.fixture
def mock_settings(monkeypatch):
    """Create mock settings for notifications"""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key")
    monkeypatch.setenv("SENDER_EMAIL", "sender@example.com")
    monkeypatch.setenv("RECIPIENT_EMAIL", "recipient@example.com")
    monkeypatch.setenv("EMAIL_PASSWORD", "test_password")
    monkeypatch.setenv("SLACK_TOKEN", "xoxb-test-token")

    return Settings()


@pytest.fixture
def notification_service(mock_settings):
    """Create notification service instance"""
    return NotificationService(mock_settings)


@pytest.fixture
def sample_report():
    """Create sample report for testing"""
    return {
        "reading_list": "# AI & Government Reports\n\n## 🔥 CRITICAL\n\nTest content here",
        "notebooklm_source": "# NotebookLM Source Document\n\nTest content",
        "metadata": {
            "model": "claude-sonnet-4",
            "input_tokens": 1000,
            "output_tokens": 2000,
            "generated_at": "2024-01-15"
        },
        "generated_at": "2024-01-15"
    }


class TestNotificationService:
    """Test NotificationService class"""

    def test_initialization(self, notification_service):
        """Test notification service initializes correctly"""
        assert notification_service is not None
        assert notification_service.settings is not None
        assert notification_service.logger is not None

    def test_format_email_text(self, notification_service, sample_report):
        """Test plain text email formatting"""
        text = notification_service._format_email_text(sample_report)

        assert "2024-01-15" in text
        assert "AI Report Scanner" in text
        assert "claude-sonnet-4" in text

    def test_format_email_html(self, notification_service, sample_report):
        """Test HTML email formatting"""
        html = notification_service._format_email_html(sample_report)

        assert "<html>" in html
        assert "2024-01-15" in html
        assert "claude-sonnet-4" in html
        assert "Weekly AI Reports Digest" in html

    def test_markdown_to_html_basic(self, notification_service):
        """Test basic markdown to HTML conversion"""
        markdown = "# Header\n\n## Subheader\n\nParagraph text"
        html = notification_service._markdown_to_html(markdown)

        assert "<h1>" in html or "<br>" in html  # Depends on markdown library availability

    @patch('smtplib.SMTP_SSL')
    def test_send_email_success(self, mock_smtp, notification_service, sample_report):
        """Test successful email sending"""
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        success = notification_service.send_email(sample_report)

        assert success
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()

    @patch('smtplib.SMTP_SSL')
    def test_send_email_with_attachments(self, mock_smtp, notification_service, sample_report, tmp_path):
        """Test email sending with attachments"""
        # Create test attachment
        attachment_path = tmp_path / "test_attachment.txt"
        attachment_path.write_text("Test attachment content")

        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        success = notification_service.send_email(
            sample_report,
            attachments=[str(attachment_path)]
        )

        assert success
        mock_server.send_message.assert_called_once()

    @patch('smtplib.SMTP_SSL')
    def test_send_email_smtp_error(self, mock_smtp, notification_service, sample_report):
        """Test email sending with SMTP error"""
        import smtplib

        # Mock SMTP server to raise error
        mock_smtp.return_value.__enter__.side_effect = smtplib.SMTPException("Connection failed")

        success = notification_service.send_email(sample_report)

        assert not success

    def test_send_email_incomplete_config(self, monkeypatch, sample_report):
        """Test email sending with incomplete configuration"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key")
        # Don't set email config

        settings = Settings()
        service = NotificationService(settings)

        success = service.send_email(sample_report)
        assert not success

    def test_extract_summary(self, notification_service, sample_report):
        """Test summary extraction for Slack"""
        summary = notification_service._extract_summary(sample_report['reading_list'])

        assert "🔥 CRITICAL" in summary
        assert len(summary) <= 2000

    def test_extract_summary_long_content(self, notification_service):
        """Test summary extraction with long content"""
        long_reading_list = "## 🔥 CRITICAL\n\n" + ("x" * 5000)
        summary = notification_service._extract_summary(long_reading_list, max_length=500)

        assert len(summary) <= 500 + 100  # Allow some buffer for markers
        assert "🔥 CRITICAL" in summary

    @patch('notifications.WebClient')
    def test_send_slack_success(self, mock_webclient, notification_service, sample_report):
        """Test successful Slack notification"""
        # Mock Slack client
        mock_client = MagicMock()
        mock_webclient.return_value = mock_client

        success = notification_service.send_slack_notification(sample_report)

        assert success
        mock_client.chat_postMessage.assert_called_once()

    @patch('notifications.WebClient')
    def test_send_slack_api_error(self, mock_webclient, notification_service, sample_report):
        """Test Slack notification with API error"""
        from slack_sdk.errors import SlackApiError

        # Mock Slack client to raise error
        mock_client = MagicMock()
        mock_client.chat_postMessage.side_effect = SlackApiError(
            message="Invalid token",
            response={"error": "invalid_auth"}
        )
        mock_webclient.return_value = mock_client

        success = notification_service.send_slack_notification(sample_report)

        assert not success

    def test_send_slack_incomplete_config(self, monkeypatch, sample_report):
        """Test Slack notification with incomplete configuration"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key")
        # Don't set Slack token

        settings = Settings()
        service = NotificationService(settings)

        success = service.send_slack_notification(sample_report)
        assert not success

    def test_attach_file_nonexistent(self, notification_service):
        """Test attaching non-existent file"""
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        notification_service._attach_file(msg, "/nonexistent/file.txt")

        # Should not raise error, just log warning
        # Check that no attachment was added
        assert len(msg.get_payload()) == 0

    def test_attach_file_success(self, notification_service, tmp_path):
        """Test successful file attachment"""
        from email.mime.multipart import MIMEMultipart

        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Test content")

        msg = MIMEMultipart()
        notification_service._attach_file(msg, str(test_file))

        # Check that attachment was added
        assert len(msg.get_payload()) == 1
