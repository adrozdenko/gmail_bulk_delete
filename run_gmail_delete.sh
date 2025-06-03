#!/bin/bash
# Gmail Bulk Delete Runner Script

echo "🚀 Starting Gmail Bulk Delete..."
echo "📁 Working directory: $(pwd)"

# Activate virtual environment
source gmail_deleter_env/bin/activate

# Check if credentials exist
if [ ! -f "credentials.json" ]; then
    echo "❌ credentials.json not found!"
    echo "📋 Please follow these steps:"
    echo "1. Go to https://console.cloud.google.com/"
    echo "2. Enable Gmail API"
    echo "3. Create OAuth 2.0 credentials"
    echo "4. Download as 'credentials.json'"
    echo "5. Place in this directory"
    exit 1
fi

# Show current configuration
echo ""
echo "📊 Current Configuration:"
cat delete_config.json | python3 -m json.tool

# Run the script
echo ""
echo "🔄 Running Gmail bulk delete..."
python3 gmail_bulk_delete.py

echo ""
echo "✅ Script completed!"