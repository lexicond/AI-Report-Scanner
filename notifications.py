"""Notification system for sending reports via email and Slack"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Dict, Optional
from config import Settings


class NotificationService:
    """Handle email and Slack notifications"""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.logger = logging.getLogger("NotificationService")

    def send_email(self, report: Dict, attachments: Optional[list] = None) -> bool:
        """
        Send report via email

        Args:
            report: Report dictionary with reading_list, notebooklm_source, metadata
            attachments: Optional list of file paths to attach

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.settings.validate_required_for_email():
            self.logger.error("Email configuration incomplete")
            return False

        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"📊 Weekly AI Reports Digest - {report['generated_at']}"
            msg["From"] = self.settings.sender_email
            msg["To"] = self.settings.recipient_email

            # Create email body
            text_content = self._format_email_text(report)
            html_content = self._format_email_html(report)

            # Attach parts
            msg.attach(MIMEText(text_content, "plain", "utf-8"))
            msg.attach(MIMEText(html_content, "html", "utf-8"))

            # Add attachments if provided
            if attachments:
                for file_path in attachments:
                    self._attach_file(msg, file_path)

            # Send email
            with smtplib.SMTP_SSL(
                self.settings.smtp_server,
                self.settings.smtp_port
            ) as server:
                server.login(
                    self.settings.sender_email,
                    self.settings.email_password
                )
                server.send_message(msg)

            self.logger.info(f"Email sent successfully to {self.settings.recipient_email}")
            return True

        except smtplib.SMTPException as e:
            self.logger.error(f"SMTP error sending email: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            return False

    def _format_email_text(self, report: Dict) -> str:
        """Format plain text email body"""
        text = f"""Weekly AI & Government Reports - {report['generated_at']}

Your weekly digest of AI and government reports is ready!

{report['reading_list'][:1000]}...

[Full reading list and NotebookLM source attached]

---
Generated using AI Report Scanner
Model: {report['metadata'].get('model', 'unknown')}
"""
        return text

    def _format_email_html(self, report: Dict) -> str:
        """Format HTML email body"""
        # Convert markdown to HTML (basic conversion)
        reading_list_html = self._markdown_to_html(report['reading_list'])

        html = f"""
<html>
<head>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        h3 {{
            color: #7f8c8d;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .footer {{
            margin-top: 40px;
            padding: 20px;
            background: #ecf0f1;
            border-radius: 5px;
            font-size: 0.9em;
            color: #7f8c8d;
        }}
        .metadata {{
            font-size: 0.85em;
            color: #95a5a6;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Weekly AI Reports Digest</h1>
        <p>{report['generated_at']}</p>
    </div>

    <div class="content">
        {reading_list_html}
    </div>

    <div class="footer">
        <p><strong>Generated using AI Report Scanner</strong></p>
        <p class="metadata">
            Model: {report['metadata'].get('model', 'unknown')}<br>
            Tokens: {report['metadata'].get('input_tokens', 0)} input /
                    {report['metadata'].get('output_tokens', 0)} output
        </p>
    </div>
</body>
</html>
"""
        return html

    def _markdown_to_html(self, markdown_text: str) -> str:
        """Basic markdown to HTML conversion"""
        try:
            import markdown
            return markdown.markdown(
                markdown_text,
                extensions=['extra', 'codehilite']
            )
        except ImportError:
            # Fallback to basic conversion if markdown library not available
            html = markdown_text.replace('\n', '<br>')
            html = html.replace('# ', '<h1>').replace('\n', '</h1>\n', 1)
            html = html.replace('## ', '<h2>').replace('\n', '</h2>\n')
            html = html.replace('### ', '<h3>').replace('\n', '</h3>\n')
            return f"<pre>{html}</pre>"

    def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """Attach file to email"""
        path = Path(file_path)
        if not path.exists():
            self.logger.warning(f"Attachment not found: {file_path}")
            return

        try:
            with open(path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())

            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {path.name}'
            )
            msg.attach(part)
            self.logger.info(f"Attached file: {path.name}")
        except Exception as e:
            self.logger.error(f"Error attaching file {file_path}: {e}")

    def send_slack_notification(self, report: Dict) -> bool:
        """
        Send report notification to Slack

        Args:
            report: Report dictionary

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.settings.validate_required_for_slack():
            self.logger.error("Slack configuration incomplete")
            return False

        try:
            from slack_sdk import WebClient
            from slack_sdk.errors import SlackApiError

            client = WebClient(token=self.settings.slack_token)

            # Extract summary from reading list
            summary = self._extract_summary(report['reading_list'])

            # Create Slack message blocks
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📊 Weekly AI Reports - {report['generated_at']}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": summary[:2800]  # Slack text limit
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"Model: {report['metadata'].get('model', 'unknown')} | "
                                   f"Tokens: {report['metadata'].get('output_tokens', 0)}"
                        }
                    ]
                }
            ]

            # Send message
            response = client.chat_postMessage(
                channel=self.settings.slack_channel,
                text=f"Weekly AI Reports - {report['generated_at']}",
                blocks=blocks
            )

            self.logger.info(f"Slack notification sent to {self.settings.slack_channel}")
            return True

        except ImportError:
            self.logger.error("slack_sdk not installed. Run: pip install slack-sdk")
            return False
        except SlackApiError as e:
            self.logger.error(f"Slack API error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error sending Slack notification: {e}")
            return False

    def _extract_summary(self, reading_list: str, max_length: int = 2000) -> str:
        """Extract summary from reading list for Slack"""
        # Find the critical section
        if "## 🔥 CRITICAL" in reading_list:
            parts = reading_list.split("## 🔥 CRITICAL", 1)
            if len(parts) > 1:
                critical_section = parts[1].split("##")[0]  # Get until next section
                return f"## 🔥 CRITICAL{critical_section[:max_length]}"

        # Fallback to first part
        return reading_list[:max_length] + "..."
