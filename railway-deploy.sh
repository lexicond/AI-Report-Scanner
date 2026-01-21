#!/bin/bash
# Script to deploy AI Report Scanner to Railway

set -e

echo "🚂 Railway Deployment Script for AI Report Scanner"
echo "=================================================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found!"
    echo ""
    echo "Please install it first:"
    echo "  npm install -g @railway/cli"
    echo ""
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "Please create .env file from .env.example:"
    echo "  cp .env.example .env"
    echo "  # Edit .env with your API keys"
    echo ""
    exit 1
fi

# Login to Railway
echo "📝 Logging into Railway..."
railway login

# Initialize project (if not already)
if [ ! -f railway.json ]; then
    echo ""
    echo "🆕 Initializing new Railway project..."
    railway init
else
    echo "✅ Railway project already initialized"
fi

# Set environment variables from .env
echo ""
echo "⚙️  Setting environment variables..."

# Read .env and set variables
while IFS='=' read -r key value; do
    # Skip comments and empty lines
    [[ $key =~ ^#.*$ ]] && continue
    [[ -z $key ]] && continue

    # Remove any surrounding quotes from value
    value=$(echo "$value" | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//")

    # Skip if value is placeholder
    if [[ $value =~ ^your_.*_here$ ]]; then
        echo "⚠️  Skipping placeholder: $key"
        continue
    fi

    echo "  Setting $key..."
    railway variables set "$key=$value"
done < .env

# Deploy
echo ""
echo "🚀 Deploying to Railway..."
railway up

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Check deployment status: railway status"
echo "2. View logs: railway logs"
echo "3. Configure cron schedule in Railway dashboard"
echo "4. Test manually: railway run python main.py"
echo ""
