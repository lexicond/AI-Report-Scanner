"""Configuration management for AI Report Scanner"""
from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings with validation"""

    # Anthropic API
    anthropic_api_key: str
    anthropic_model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 16000

    # Email settings
    sender_email: Optional[str] = None
    recipient_email: Optional[str] = None
    email_password: Optional[str] = None
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 465

    # Slack settings
    slack_token: Optional[str] = None
    slack_channel: str = "#ai-reports"

    # GitHub settings
    save_to_github: bool = False
    github_token: Optional[str] = None

    # Application settings
    log_level: str = "INFO"
    dry_run: bool = False
    max_reports: int = 25
    search_days_back: int = 7

    # Output directories
    output_dir: Path = Path("output")
    reports_dir: Path = Path("reports")
    logs_dir: Path = Path("logs")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def validate_required_for_email(self) -> bool:
        """Check if email configuration is complete"""
        return all([
            self.sender_email,
            self.recipient_email,
            self.email_password
        ])

    def validate_required_for_slack(self) -> bool:
        """Check if Slack configuration is complete"""
        return bool(self.slack_token)

    def create_directories(self):
        """Create necessary directories if they don't exist"""
        for directory in [self.output_dir, self.reports_dir, self.logs_dir]:
            directory.mkdir(exist_ok=True)


def get_settings() -> Settings:
    """Get validated settings instance"""
    return Settings()
