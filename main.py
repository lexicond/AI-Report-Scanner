#!/usr/bin/env python3
"""
AI Report Scanner - Weekly automated report curation
Main entry point for the application
"""
import sys
import logging
from pathlib import Path
from config import get_settings
from scanner import ReportScanner
from notifications import NotificationService


def setup_logging(log_level: str):
    """Setup root logging configuration"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main execution function"""
    print("=" * 70)
    print("🤖 AI Report Scanner - Weekly Government AI Report Curation")
    print("=" * 70)
    print()

    # Load settings
    try:
        settings = get_settings()
        setup_logging(settings.log_level)
        logger = logging.getLogger(__name__)

        # Create necessary directories
        settings.create_directories()

        logger.info("Configuration loaded successfully")
        logger.info(f"Mode: {'DRY RUN' if settings.dry_run else 'PRODUCTION'}")
        logger.info(f"Search period: Last {settings.search_days_back} days")

    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        print("\nPlease ensure:")
        print("1. You have created a .env file (copy from .env.example)")
        print("2. You have set ANTHROPIC_API_KEY in .env")
        print("3. All required dependencies are installed (pip install -r requirements.txt)")
        sys.exit(1)

    # Initialize scanner
    try:
        logger.info("Initializing report scanner...")
        scanner = ReportScanner(settings)
    except Exception as e:
        logger.error(f"Failed to initialize scanner: {e}")
        sys.exit(1)

    # Generate report
    try:
        logger.info("Starting report generation...")
        print("\n🔍 Searching for reports...")
        print("This may take a few minutes...\n")

        report = scanner.generate_report()

        print("✅ Report generated successfully!")
        print()

        # Validate report
        logger.info("Validating report...")
        is_valid, issues = scanner.validate_report(report)

        if not is_valid:
            logger.warning(f"Report validation found issues: {issues}")
            print(f"⚠️  Report validation warnings: {len(issues)}")
            for issue in issues:
                print(f"   - {issue}")
        else:
            logger.info("Report validation passed")
            print("✅ Report validation passed")

        print()

        # Display summary
        print("📊 Report Summary:")
        print(f"   Generated: {report['generated_at']}")
        print(f"   Model: {report['metadata'].get('model', 'unknown')}")
        print(f"   Input tokens: {report['metadata'].get('input_tokens', 0):,}")
        print(f"   Output tokens: {report['metadata'].get('output_tokens', 0):,}")
        print()

        # Show where files are saved
        print("💾 Output files saved to:")
        print(f"   Reading List: reports/reading_list_{report['generated_at']}.md")
        if report['notebooklm_source']:
            print(f"   NotebookLM: reports/notebooklm_{report['generated_at']}.md")
        print(f"   Metadata: output/metadata_{report['generated_at']}.json")
        print()

    except Exception as e:
        logger.error(f"Report generation failed: {e}", exc_info=True)
        print(f"\n❌ Error generating report: {e}")
        sys.exit(1)

    # Send notifications
    if not settings.dry_run:
        notification_service = NotificationService(settings)

        # Email notification
        if settings.validate_required_for_email():
            try:
                logger.info("Sending email notification...")
                print("📧 Sending email notification...")

                # Prepare attachments
                attachments = [
                    f"reports/reading_list_{report['generated_at']}.md"
                ]
                if report['notebooklm_source']:
                    attachments.append(f"reports/notebooklm_{report['generated_at']}.md")

                success = notification_service.send_email(report, attachments)
                if success:
                    print(f"✅ Email sent to {settings.recipient_email}")
                else:
                    print("❌ Email sending failed (check logs)")
            except Exception as e:
                logger.error(f"Email notification error: {e}")
                print(f"❌ Email error: {e}")
        else:
            logger.info("Email not configured, skipping")
            print("ℹ️  Email not configured - reports saved locally to reports/ folder")
            print("   To enable email: Set SENDER_EMAIL, RECIPIENT_EMAIL, EMAIL_PASSWORD")
            print("   Alternative: Check reports/ folder for markdown files")

        # Slack notification
        if settings.validate_required_for_slack():
            try:
                logger.info("Sending Slack notification...")
                print("💬 Sending Slack notification...")
                success = notification_service.send_slack_notification(report)
                if success:
                    print(f"✅ Slack message sent to {settings.slack_channel}")
                else:
                    print("❌ Slack sending failed (check logs)")
            except Exception as e:
                logger.error(f"Slack notification error: {e}")
                print(f"❌ Slack error: {e}")
        else:
            logger.info("Slack not configured, skipping")

        print()

    # Final message
    print("=" * 70)
    print("✅ AI Report Scanner completed successfully!")
    print("=" * 70)
    print()
    print("📁 Your reports are ready:")
    print(f"   📄 Reading List: reports/reading_list_{report['generated_at']}.md")
    if report['notebooklm_source']:
        print(f"   🎙️  NotebookLM: reports/notebooklm_{report['generated_at']}.md")
    print()
    print("Next steps:")
    print("1. Open reports/ folder to read your curated report")
    print("2. Upload notebooklm_*.md to NotebookLM for audio summary")
    if settings.validate_required_for_email():
        print("3. Check your email for the digest")
    else:
        print("3. Optional: Configure email to receive automatic delivery")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
