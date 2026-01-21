"""Tests for configuration management"""
import pytest
from pathlib import Path
import os
from config import Settings, get_settings


class TestSettings:
    """Test Settings class"""

    def test_settings_from_env(self, monkeypatch):
        """Test loading settings from environment variables"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key_123")
        monkeypatch.setenv("SENDER_EMAIL", "test@example.com")
        monkeypatch.setenv("RECIPIENT_EMAIL", "recipient@example.com")

        settings = Settings()

        assert settings.anthropic_api_key == "test_key_123"
        assert settings.sender_email == "test@example.com"
        assert settings.recipient_email == "recipient@example.com"

    def test_default_values(self, monkeypatch):
        """Test default configuration values"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key")

        settings = Settings()

        assert settings.anthropic_model == "claude-sonnet-4-20250514"
        assert settings.max_tokens == 16000
        assert settings.log_level == "INFO"
        assert settings.dry_run is False
        assert settings.max_reports == 25
        assert settings.search_days_back == 7

    def test_email_validation(self, monkeypatch):
        """Test email configuration validation"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key")

        # Test with incomplete email config
        settings = Settings()
        assert not settings.validate_required_for_email()

        # Test with complete email config
        monkeypatch.setenv("SENDER_EMAIL", "sender@example.com")
        monkeypatch.setenv("RECIPIENT_EMAIL", "recipient@example.com")
        monkeypatch.setenv("EMAIL_PASSWORD", "password123")

        settings = Settings()
        assert settings.validate_required_for_email()

    def test_slack_validation(self, monkeypatch):
        """Test Slack configuration validation"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key")

        # Without Slack token
        settings = Settings()
        assert not settings.validate_required_for_slack()

        # With Slack token
        monkeypatch.setenv("SLACK_TOKEN", "xoxb-test-token")
        settings = Settings()
        assert settings.validate_required_for_slack()

    def test_create_directories(self, tmp_path, monkeypatch):
        """Test directory creation"""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key")

        # Use tmp_path for testing
        output_dir = tmp_path / "output"
        reports_dir = tmp_path / "reports"
        logs_dir = tmp_path / "logs"

        settings = Settings()
        settings.output_dir = output_dir
        settings.reports_dir = reports_dir
        settings.logs_dir = logs_dir

        # Directories should not exist yet
        assert not output_dir.exists()
        assert not reports_dir.exists()
        assert not logs_dir.exists()

        # Create directories
        settings.create_directories()

        # Directories should now exist
        assert output_dir.exists()
        assert reports_dir.exists()
        assert logs_dir.exists()

    def test_missing_api_key_raises_error(self):
        """Test that missing API key raises validation error"""
        with pytest.raises(Exception):
            Settings()
