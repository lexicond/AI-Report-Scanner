#!/usr/bin/env python3
"""
Lightweight tracking server for report interactions

Provides:
1. Click tracking API
2. Rating interface
3. Analytics dashboard
4. Report viewer with tracking

Usage:
    python tracking_server.py

Then access at: http://localhost:5000
"""

from flask import Flask, request, jsonify, render_template_string, redirect
from flask_cors import CORS
from pathlib import Path
import json
from datetime import datetime, timedelta
import uuid

from prompt_evolution import InteractionTracker, RewardFunction

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for click tracking

tracker = InteractionTracker()
reward_fn = RewardFunction()

# In-memory session tracking (use Redis in production)
sessions = {}


# HTML Templates
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Report Scanner - Analytics Dashboard</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .report-list {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .report-item {
            padding: 15px;
            border-bottom: 1px solid #eee;
        }
        .report-item:last-child {
            border-bottom: none;
        }
        .report-title {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        .report-metrics {
            display: flex;
            gap: 20px;
            font-size: 0.9em;
            color: #666;
        }
        .metric {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .rating-buttons {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        button {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9em;
        }
        .btn-positive {
            background: #4CAF50;
            color: white;
        }
        .btn-negative {
            background: #f44336;
            color: white;
        }
        .btn-view {
            background: #2196F3;
            color: white;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 AI Report Scanner - Analytics Dashboard</h1>
        <p>Track report performance and user engagement</p>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">{{ total_reports }}</div>
            <div class="stat-label">Total Reports</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ total_clicks }}</div>
            <div class="stat-label">Total Clicks</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ avg_ctr }}%</div>
            <div class="stat-label">Click-Through Rate</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ avg_rating }}</div>
            <div class="stat-label">Avg Rating (1-5)</div>
        </div>
    </div>

    <div class="report-list">
        <h2>📊 Recent Reports</h2>
        {% for report in reports %}
        <div class="report-item" id="report-{{ report.id }}">
            <div class="report-title">{{ report.title }}</div>
            <div class="report-metrics">
                <div class="metric">👆 {{ report.clicks }} clicks</div>
                <div class="metric">⏱️ {{ report.avg_time }}s avg time</div>
                <div class="metric">👍 {{ report.positive_ratings }}</div>
                <div class="metric">👎 {{ report.negative_ratings }}</div>
            </div>
            <div class="rating-buttons">
                <button class="btn-view" onclick="trackClick('{{ report.id }}')">
                    📖 View Report
                </button>
                <button class="btn-positive" onclick="rate('{{ report.id }}', 1)">
                    👍 Helpful
                </button>
                <button class="btn-negative" onclick="rate('{{ report.id }}', -1)">
                    👎 Not Helpful
                </button>
            </div>
        </div>
        {% endfor %}
    </div>

    <script>
        function trackClick(reportId) {
            fetch(`/api/track/click`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    report_id: reportId,
                    user_id: getUserId()
                })
            }).then(() => {
                window.open(`/report/${reportId}`, '_blank');
            });
        }

        function rate(reportId, rating) {
            fetch(`/api/track/rating`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    report_id: reportId,
                    user_id: getUserId(),
                    rating: rating
                })
            }).then(() => {
                alert(rating > 0 ? 'Thanks for your feedback!' : 'Thanks, we\'ll improve!');
                location.reload();
            });
        }

        function getUserId() {
            let userId = localStorage.getItem('user_id');
            if (!userId) {
                userId = 'user_' + Math.random().toString(36).substr(2, 9);
                localStorage.setItem('user_id', userId);
            }
            return userId;
        }
    </script>
</body>
</html>
"""

REPORT_VIEWER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ report.title }} - AI Report Scanner</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .content {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .meta {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 20px;
        }
        .rating-prompt {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
            text-align: center;
        }
        button {
            padding: 10px 20px;
            margin: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1em;
        }
        .btn-positive {
            background: #4CAF50;
            color: white;
        }
        .btn-negative {
            background: #f44336;
            color: white;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ report.title }}</h1>
        <div class="meta">
            {{ report.source }} | {{ report.date }} | {{ report.length }}
        </div>
    </div>

    <div class="content">
        {{ report.content | safe }}
    </div>

    <div class="rating-prompt">
        <h3>Was this report helpful?</h3>
        <p>Your feedback helps us improve report curation</p>
        <button class="btn-positive" onclick="rate(1)">👍 Yes, very helpful</button>
        <button class="btn-negative" onclick="rate(-1)">👎 Not relevant</button>
    </div>

    <script>
        let startTime = Date.now();

        // Track dwell time when user leaves
        window.addEventListener('beforeunload', function() {
            let dwellTime = (Date.now() - startTime) / 1000;
            navigator.sendBeacon('/api/track/dwell', JSON.stringify({
                report_id: '{{ report.id }}',
                user_id: getUserId(),
                seconds: dwellTime
            }));
        });

        function rate(rating) {
            fetch('/api/track/rating', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    report_id: '{{ report.id }}',
                    user_id: getUserId(),
                    rating: rating
                })
            }).then(() => {
                alert(rating > 0 ? 'Thanks for your feedback!' : 'Thanks for your feedback!');
                window.close();
            });
        }

        function getUserId() {
            let userId = localStorage.getItem('user_id');
            if (!userId) {
                userId = 'user_' + Math.random().toString(36).substr(2, 9);
                localStorage.setItem('user_id', userId);
            }
            return userId;
        }
    </script>
</body>
</html>
"""


# API Routes
@app.route('/')
def dashboard():
    """Show analytics dashboard"""
    # Load recent reports (placeholder - would load from database)
    reports = _get_recent_reports()

    # Calculate stats
    total_clicks = sum(r['clicks'] for r in reports)
    total_ratings = sum(r['positive_ratings'] + r['negative_ratings'] for r in reports)

    stats = {
        'total_reports': len(reports),
        'total_clicks': total_clicks,
        'avg_ctr': round((total_clicks / len(reports) * 100) if reports else 0, 1),
        'avg_rating': round(
            sum(r['positive_ratings'] - r['negative_ratings'] for r in reports) / len(reports)
            if reports else 0, 1
        )
    }

    return render_template_string(DASHBOARD_TEMPLATE, reports=reports, **stats)


@app.route('/report/<report_id>')
def view_report(report_id):
    """View a single report with tracking"""
    # Load report details (placeholder)
    report = _get_report_details(report_id)

    if not report:
        return "Report not found", 404

    return render_template_string(REPORT_VIEWER_TEMPLATE, report=report)


@app.route('/api/track/click', methods=['POST'])
def track_click():
    """Track report click"""
    data = request.json
    report_id = data.get('report_id')
    user_id = data.get('user_id')

    if not report_id or not user_id:
        return jsonify({'error': 'Missing parameters'}), 400

    tracker.track_click(report_id, user_id)

    return jsonify({'status': 'success'})


@app.route('/api/track/dwell', methods=['POST'])
def track_dwell():
    """Track dwell time"""
    data = request.json
    report_id = data.get('report_id')
    user_id = data.get('user_id')
    seconds = data.get('seconds')

    if not all([report_id, user_id, seconds]):
        return jsonify({'error': 'Missing parameters'}), 400

    tracker.track_dwell_time(report_id, user_id, float(seconds))

    return jsonify({'status': 'success'})


@app.route('/api/track/rating', methods=['POST'])
def track_rating():
    """Track user rating"""
    data = request.json
    report_id = data.get('report_id')
    user_id = data.get('user_id')
    rating = data.get('rating')

    if not all([report_id, user_id, rating is not None]):
        return jsonify({'error': 'Missing parameters'}), 400

    tracker.track_rating(report_id, user_id, int(rating))

    return jsonify({'status': 'success'})


@app.route('/api/metrics/<report_id>')
def get_metrics(report_id):
    """Get metrics for a specific report"""
    metrics = tracker.get_report_metrics(report_id)
    return jsonify(metrics)


@app.route('/api/reports')
def list_reports():
    """List all tracked reports"""
    reports = _get_recent_reports()
    return jsonify(reports)


# Helper functions
def _get_recent_reports():
    """Load recent reports with metrics"""
    # Placeholder - would load from actual report storage
    # For now, return mock data

    reports_dir = Path("reports")
    if not reports_dir.exists():
        return []

    reports = []
    for report_file in sorted(reports_dir.glob("reading_list_*.md"))[:10]:
        report_id = report_file.stem.replace("reading_list_", "")

        # Get metrics from tracker
        metrics = tracker.get_report_metrics(report_id)

        reports.append({
            'id': report_id,
            'title': f"AI Reports Digest - {report_id}",
            'clicks': metrics.get('clicks', 0),
            'avg_time': metrics.get('avg_dwell_time', 0),
            'positive_ratings': metrics.get('ratings_positive', 0),
            'negative_ratings': metrics.get('ratings_negative', 0)
        })

    return reports


def _get_report_details(report_id):
    """Load full report details"""
    report_file = Path(f"reports/reading_list_{report_id}.md")

    if not report_file.exists():
        return None

    with open(report_file) as f:
        content = f.read()

    # Convert markdown to HTML (basic)
    content_html = content.replace('\n', '<br>')

    return {
        'id': report_id,
        'title': f"AI Reports Digest - {report_id}",
        'source': "AI Report Scanner",
        'date': report_id,
        'length': f"{len(content)} chars",
        'content': content_html
    }


if __name__ == '__main__':
    print("🚀 Starting AI Report Scanner - Tracking Server")
    print("📊 Dashboard: http://localhost:5000")
    print("📈 API: http://localhost:5000/api")
    print("\nPress Ctrl+C to stop")

    app.run(host='0.0.0.0', port=5000, debug=True)
