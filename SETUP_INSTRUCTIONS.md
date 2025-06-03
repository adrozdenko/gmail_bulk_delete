# Gmail Bulk Delete Setup Instructions

## Prerequisites
- Python 3.7 or higher
- Google Cloud Console account
- Gmail account

## Step 1: Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

## Step 2: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop application"
4. Name it "Gmail Bulk Delete"
5. Download the JSON file as `credentials.json`
6. Place `credentials.json` in the same directory as the script

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configuration (Already Set for Your Needs)

Your `delete_config.json` is configured to:
- Delete emails older than 6 months (180 days)
- Keep ALL emails with attachments (photos, videos, documents)
- Keep important and starred emails
- Start in dry-run mode for safety

```json
{
  "older_than_days": 180,
  "exclude_with_attachments": true,
  "exclude_important": true,
  "exclude_starred": true,
  "dry_run": true
}
```

## Step 5: Run the Script

**Easy way (recommended):**
```bash
./run_gmail_delete.sh
```

**Manual way:**
```bash
source gmail_deleter_env/bin/activate
python3 gmail_bulk_delete.py
```

**After reviewing dry run results:**
1. Edit `delete_config.json` and set `"dry_run": false`
2. Run the script again to actually delete emails

## Safety Features

- **Dry run mode**: Test your criteria without deleting anything
- **Preview**: Shows first 5 emails that match criteria
- **Confirmation**: Asks for confirmation before actual deletion
- **Exclusions**: Never deletes important, starred, trash, or spam emails
- **Batch processing**: Deletes in batches for reliability

## Configuration Options

| Option | Description | Example |
|--------|-------------|---------|
| `older_than_days` | Delete emails older than X days | `180` |
| `from_addresses` | Delete from specific senders | `["spam@example.com"]` |
| `subject_contains` | Delete emails with keywords in subject | `["Sale", "Offer"]` |
| `labels` | Delete emails with specific Gmail labels | `["promotions"]` |
| `size_larger_than_mb` | Delete large emails (MB) | `10` |
| `exclude_important` | Skip important emails | `true` |
| `exclude_starred` | Skip starred emails | `true` |
| `exclude_with_attachments` | Skip emails with attachments (photos/videos/docs) | `true` |
| `dry_run` | Test mode only | `true` |

## Common Use Cases

### Delete Old Newsletters
```json
{
  "older_than_days": 90,
  "subject_contains": ["Newsletter", "Unsubscribe"],
  "dry_run": true
}
```

### Clean Up Promotions
```json
{
  "labels": ["promotions"],
  "older_than_days": 30,
  "dry_run": true
}
```

### Remove Large Attachments
```json
{
  "size_larger_than_mb": 25,
  "older_than_days": 180,
  "dry_run": true
}
```

## Troubleshooting

**Authentication Error:**
- Make sure `credentials.json` is in the correct location
- Check if Gmail API is enabled in Google Cloud Console

**No Emails Found:**
- Check your search criteria in `delete_config.json`
- Try broader criteria first

**Permission Denied:**
- Ensure OAuth consent screen is configured
- Add your email as a test user if app is in testing mode

## Security Notes

- Keep `credentials.json` secure and never share it
- The script only requests necessary permissions
- `token.pickle` stores your authentication locally
- Always test with `dry_run: true` first