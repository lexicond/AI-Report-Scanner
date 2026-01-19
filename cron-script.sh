#!/bin/sh
# Cron script to run AI Report Scanner weekly
# Runs every Monday at 9:00 AM

echo "Starting AI Report Scanner at $(date)"

# Run the scanner container
docker exec ai-report-scanner python main.py

echo "AI Report Scanner completed at $(date)"
