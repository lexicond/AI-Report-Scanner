"""Core AI Report Scanner - Weekly report generation with Claude"""
import anthropic
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from config import Settings


class ReportScanner:
    """Automated weekly AI report scanning using Claude"""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.logger = self._setup_logger()
        self.seen_reports_file = settings.output_dir / "seen_reports.json"
        self._load_seen_reports()

    def _setup_logger(self) -> logging.Logger:
        """Configure logging"""
        logger = logging.getLogger("ReportScanner")
        logger.setLevel(self.settings.log_level)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.settings.log_level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler
        self.settings.logs_dir.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(
            self.settings.logs_dir / f"scanner_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    def _load_seen_reports(self):
        """Load previously seen reports to avoid duplicates"""
        if self.seen_reports_file.exists():
            with open(self.seen_reports_file, 'r') as f:
                self.seen_reports = set(json.load(f))
        else:
            self.seen_reports = set()
        self.logger.info(f"Loaded {len(self.seen_reports)} previously seen reports")

    def _save_seen_reports(self):
        """Save seen reports to file"""
        self.settings.output_dir.mkdir(exist_ok=True)
        with open(self.seen_reports_file, 'w') as f:
            json.dump(list(self.seen_reports), f, indent=2)
        self.logger.info(f"Saved {len(self.seen_reports)} seen reports")

    def _calculate_date_range(self) -> Tuple[datetime, datetime, datetime]:
        """Calculate search date range"""
        today = datetime.now()
        start_date = today - timedelta(days=self.settings.search_days_back)
        return today, start_date, today

    def _load_prompt_template(self) -> str:
        """Load search prompt template"""
        prompt_file = Path("search_prompt.txt")
        if not prompt_file.exists():
            raise FileNotFoundError(f"Search prompt template not found: {prompt_file}")

        with open(prompt_file, 'r') as f:
            return f.read()

    def _format_prompt(self, template: str, current_date: str, start_date: str, end_date: str) -> str:
        """Format prompt with dates using safe string replacement"""
        date_range = f"{start_date} to {end_date}"

        # Use string replacement to avoid conflicts with Claude's output template placeholders
        template = template.replace("{current_date}", current_date)
        template = template.replace("{start_date}", start_date)
        template = template.replace("{end_date}", end_date)
        template = template.replace("{date_range}", date_range)
        template = template.replace("{date}", current_date)

        return template

    def generate_report(self) -> Dict[str, any]:
        """
        Main method to generate weekly report using Claude

        Returns:
            Dict with reading_list, notebooklm_source, metadata
        """
        self.logger.info("Starting weekly report generation")

        # Calculate dates
        today, start_date, end_date = self._calculate_date_range()
        current_date = today.strftime("%Y-%m-%d")
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        self.logger.info(f"Search period: {start_date_str} to {end_date_str}")

        # Load and format prompt
        try:
            template = self._load_prompt_template()
            prompt = self._format_prompt(template, current_date, start_date_str, end_date_str)
        except Exception as e:
            self.logger.error(f"Error loading prompt: {e}")
            raise

        # Check dry run mode
        if self.settings.dry_run:
            self.logger.info("DRY RUN MODE - Skipping actual API call")
            return self._generate_mock_report(current_date)

        # Call Claude API with web search enabled
        try:
            self.logger.info("Calling Claude API with web search...")
            message = self.client.messages.create(
                model=self.settings.anthropic_model,
                max_tokens=self.settings.max_tokens,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                # Enable web search tool
                tools=[{
                    "type": "web_search_20250305",
                    "name": "web_search"
                }]
            )

            self.logger.info("Successfully received response from Claude")

            # Extract content
            reading_list, notebooklm_source = self._parse_response(message)

            # Extract metadata
            metadata = self._extract_metadata(message, current_date)

            result = {
                "reading_list": reading_list,
                "notebooklm_source": notebooklm_source,
                "metadata": metadata,
                "generated_at": current_date
            }

            # Save outputs
            self._save_outputs(result)

            self.logger.info("Report generation completed successfully")
            return result

        except anthropic.APIError as e:
            self.logger.error(f"Anthropic API error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during report generation: {e}")
            raise

    def _parse_response(self, message) -> Tuple[str, str]:
        """Parse Claude's response into reading list and NotebookLM source"""
        full_text = ""

        # Extract text from response
        for content_block in message.content:
            if content_block.type == "text":
                full_text += content_block.text

        # Split into two outputs
        reading_list = ""
        notebooklm_source = ""

        # Look for NotebookLM section
        if "# NotebookLM Source Document" in full_text:
            parts = full_text.split("# NotebookLM Source Document", 1)
            reading_list = parts[0].strip()
            notebooklm_source = ("# NotebookLM Source Document" + parts[1]).strip()
        else:
            # If no NotebookLM section found, use full text as reading list
            reading_list = full_text.strip()
            self.logger.warning("No NotebookLM section found in response")

        return reading_list, notebooklm_source

    def _extract_metadata(self, message, current_date: str) -> Dict:
        """Extract metadata from Claude's response"""
        return {
            "model": message.model,
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens,
            "stop_reason": message.stop_reason,
            "generated_at": current_date,
            "search_days_back": self.settings.search_days_back
        }

    def _save_outputs(self, result: Dict):
        """Save outputs to files"""
        timestamp = result['generated_at']
        output_dir = self.settings.output_dir
        reports_dir = self.settings.reports_dir

        # Create directories
        output_dir.mkdir(exist_ok=True)
        reports_dir.mkdir(exist_ok=True)

        # Save reading list
        reading_list_file = reports_dir / f"reading_list_{timestamp}.md"
        with open(reading_list_file, 'w') as f:
            f.write(result['reading_list'])
        self.logger.info(f"Saved reading list to {reading_list_file}")

        # Save NotebookLM source
        if result['notebooklm_source']:
            notebooklm_file = reports_dir / f"notebooklm_{timestamp}.md"
            with open(notebooklm_file, 'w') as f:
                f.write(result['notebooklm_source'])
            self.logger.info(f"Saved NotebookLM source to {notebooklm_file}")

        # Save metadata
        metadata_file = output_dir / f"metadata_{timestamp}.json"
        with open(metadata_file, 'w') as f:
            json.dump(result['metadata'], f, indent=2)
        self.logger.info(f"Saved metadata to {metadata_file}")

        # Save full result
        full_result_file = output_dir / f"report_{timestamp}.json"
        with open(full_result_file, 'w') as f:
            # Create a serializable version
            serializable_result = {
                "reading_list": result['reading_list'],
                "notebooklm_source": result['notebooklm_source'],
                "metadata": result['metadata'],
                "generated_at": result['generated_at']
            }
            json.dump(serializable_result, f, indent=2)
        self.logger.info(f"Saved full result to {full_result_file}")

    def _generate_mock_report(self, current_date: str) -> Dict:
        """Generate mock report for dry run mode"""
        mock_reading_list = f"""# AI & Government Reports: Week of {current_date}

## 🔥 CRITICAL - Read Immediately (2 reports)

### Mock Report: The Future of AI in Government
**Source**: Institute for Government | **Published**: {current_date} | **Length**: 45 pages
**Link**: https://example.com/report1

**Why Critical**: This is a mock report for testing purposes.

**Key Takeaways**:
- Mock finding 1
- Mock finding 2
- Mock finding 3

**Relevance to Your Work**:
- Government Initiatives: Highly relevant
- Frontier Labs: Some relevance

**Actionable Insights**: Test the system

**Quote to Remember**: "This is a test quote"

---

## WEEKLY SYNTHESIS

### Cross-Cutting Themes
- Theme 1: Testing
- Theme 2: Validation
- Theme 3: Deployment
"""

        mock_notebooklm = f"""# NotebookLM Source Document: AI & Gov Reports Week of {current_date}

## Introduction
This is a mock NotebookLM source document for testing purposes.

## Critical Report 1: Mock Report

**Context**: This is a test report

**Main Argument**: Testing the system

**Key Evidence**:
- Data point 1: Test data
- Data point 2: More test data

**Why This Matters for UK Government AI**: This is for testing
"""

        return {
            "reading_list": mock_reading_list,
            "notebooklm_source": mock_notebooklm,
            "metadata": {
                "model": "mock",
                "input_tokens": 0,
                "output_tokens": 0,
                "stop_reason": "mock",
                "generated_at": current_date,
                "search_days_back": self.settings.search_days_back
            },
            "generated_at": current_date
        }

    def validate_report(self, report: Dict) -> Tuple[bool, List[str]]:
        """
        Validate generated report structure and content

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        # Check required keys
        required_keys = ["reading_list", "notebooklm_source", "metadata", "generated_at"]
        for key in required_keys:
            if key not in report:
                issues.append(f"Missing required key: {key}")

        # Validate reading list
        if "reading_list" in report:
            reading_list = report["reading_list"]
            if not reading_list or len(reading_list) < 100:
                issues.append("Reading list is too short or empty")
            if "# AI & Government Reports" not in reading_list:
                issues.append("Reading list missing expected header")

        # Validate NotebookLM source
        if "notebooklm_source" in report:
            notebooklm = report["notebooklm_source"]
            if notebooklm and "# NotebookLM Source Document" not in notebooklm:
                issues.append("NotebookLM source missing expected header")

        # Validate metadata
        if "metadata" in report:
            metadata = report["metadata"]
            required_metadata = ["model", "generated_at"]
            for key in required_metadata:
                if key not in metadata:
                    issues.append(f"Metadata missing required key: {key}")

        is_valid = len(issues) == 0
        return is_valid, issues
