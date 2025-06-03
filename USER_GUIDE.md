# Gmail Bulk Delete Tool - Complete User Guide

A comprehensive guide to set up and use the Gmail bulk delete tool to safely clean up your Gmail account while preserving important emails and attachments.

## 🎯 What This Tool Does

✅ **Safely deletes old emails** based on your criteria  
✅ **Preserves emails with attachments** (photos, videos, documents)  
✅ **Keeps important and starred emails** safe  
✅ **Moves emails to trash** (not permanent deletion - can be recovered)  
✅ **Processes large volumes efficiently** in manageable batches  

## 📋 Prerequisites

- **macOS, Windows, or Linux** computer
- **Python 3.9+** installed
- **Gmail account** 
- **Google Cloud Console** access (free)
- **Terminal/Command Prompt** access

## 🚀 Complete Setup Guide

### Step 1: Download the Tool

```bash
# Clone or download the project
git clone https://github.com/adrozdenko/gmail_bulk_delete.git
cd gmail_bulk_delete

# OR download ZIP and extract to a folder
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install click rich pydantic python-dotenv pydantic-settings
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 3: Google Cloud Console Setup

#### A. Create Google Cloud Project

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Sign in** with your Gmail account
3. **Create New Project**:
   - Click "Select a project" dropdown
   - Click "NEW PROJECT"
   - **Project name**: "Gmail Bulk Delete"
   - Click "CREATE"

#### B. Enable Gmail API

1. **Navigate to APIs**:
   - Go to "APIs & Services" → "Library"
2. **Enable Gmail API**:
   - Search for "Gmail API"
   - Click on "Gmail API"
   - Click "ENABLE"

#### C. Configure OAuth Consent Screen

1. **Go to OAuth consent screen**:
   - "APIs & Services" → "OAuth consent screen"

2. **Choose User Type**:
   - Select "External"
   - Click "CREATE"

3. **App Information**:
   - **App name**: "Gmail Bulk Delete Tool"
   - **User support email**: Your email address
   - **Developer contact information**: Your email address

4. **Scopes** (Important):
   - Click "ADD OR REMOVE SCOPES"
   - Search for "Gmail API"
   - Select these scopes:
     - `https://www.googleapis.com/auth/gmail.readonly`
     - `https://www.googleapis.com/auth/gmail.modify`
   - Click "UPDATE"

5. **Test Users**:
   - Click "ADD USERS"
   - Enter your Gmail address
   - Click "SAVE"

6. **Review and Save**:
   - Click "SAVE AND CONTINUE" through all steps

#### D. Create OAuth Credentials

1. **Go to Credentials**:
   - "APIs & Services" → "Credentials"

2. **Create OAuth Client ID**:
   - Click "CREATE CREDENTIALS" → "OAuth client ID"
   - **Application type**: "Desktop application"
   - **Name**: "Gmail Bulk Delete Tool"
   - Click "CREATE"

3. **Download Credentials**:
   - Click the download button (⬇️) next to your new OAuth client
   - Save as `credentials.json`
   - **Move this file to your project folder**

### Step 4: Configure Deletion Rules

Edit `delete_config.json` to set your preferences:

```json
{
  "older_than_days": 180,
  "exclude_with_attachments": true,
  "exclude_important": true,
  "exclude_starred": true,
  "dry_run": true
}
```

**Configuration Options:**
- `older_than_days`: Delete emails older than X days (180 = 6 months)
- `exclude_with_attachments`: Keep emails with photos/videos/documents
- `exclude_important`: Keep important emails
- `exclude_starred`: Keep starred emails  
- `dry_run`: Test mode (true = safe preview, false = actual deletion)

## 🔧 How to Use the Tool

### Option 1: Quick and Easy (Recommended)

**Step 1: Test with Safe Preview**
```bash
# Activate environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Run safe preview
python gmail_bulk_delete.py
```

**What happens:**
- Opens browser for Gmail authorization
- Shows preview of emails that would be deleted
- **No actual deletion** in dry-run mode

**Step 2: Actual Deletion (when ready)**
```bash
# Edit config to disable dry-run
# Change "dry_run": true to "dry_run": false in delete_config.json

# Run deletion
python gmail_bulk_delete.py
```

### Option 2: Advanced CLI Interface

**List available rules:**
```bash
python -m src.main rules
```

**Preview with specific rule:**
```bash
python -m src.main preview --rule keep_attachments_6months
```

**Execute deletion:**
```bash
python -m src.main delete --rule keep_attachments_6months --no-dry-run
```

### Option 3: Large Volume Cleanup

For accounts with many emails (thousands):

```bash
# Use optimized batch processor
python delete_in_chunks.py
```

This processes emails in small batches to avoid timeouts.

## 🛡️ Safety Features

### What's Protected (Never Deleted)
- ✅ **Emails with attachments** (photos, videos, documents)
- ✅ **Important emails** (marked as important)
- ✅ **Starred emails** (your saved emails)
- ✅ **Emails in trash** (already deleted)
- ✅ **Emails in spam** (already filtered)

### Safety Measures
- ✅ **Dry-run mode by default** - preview before deletion
- ✅ **Moves to trash** (not permanent deletion)
- ✅ **Confirmation prompts** before bulk operations
- ✅ **Batch processing** prevents overwhelming the system
- ✅ **Error recovery** continues if individual emails fail

## 📊 What Gets Cleaned Up

**Typical emails deleted:**
- 📧 Old newsletters and promotional emails
- 💻 GitHub/development notifications  
- 📈 Marketing emails from online services
- 🔔 Social media notifications
- 📋 Automated system emails
- 📰 News and update emails
- 🎯 Any email older than your specified time period

## 🔍 Troubleshooting

### "Credentials file not found"
- Ensure `credentials.json` is in the project folder
- Re-download from Google Cloud Console if needed

### "Access blocked" during OAuth
- Add your email as a test user in OAuth consent screen
- Ensure Gmail API is enabled
- Check that OAuth client is created correctly

### "Insufficient authentication scopes"
- Verify Gmail scopes are added in OAuth consent screen
- Delete `token.pickle` and re-authenticate
- Ensure both `gmail.readonly` and `gmail.modify` scopes are granted

### "Rate limit exceeded"
- Use the chunk-based deletion script: `python delete_in_chunks.py`
- Add delays between batches
- Process smaller batches at a time

### Tool times out with large volumes
- Use `delete_in_chunks.py` for better handling
- Process in multiple sessions
- Check internet connection stability

## 📈 Performance Tips

### For Small Cleanup (< 1,000 emails)
```bash
python gmail_bulk_delete.py
```

### For Medium Cleanup (1,000 - 10,000 emails)
```bash
python gmail_bulk_delete_optimized.py
```

### For Large Cleanup (> 10,000 emails)
```bash
python delete_in_chunks.py
# Run multiple times until complete
```

## 🔄 Regular Maintenance

**Monthly cleanup routine:**
1. Run preview to see what would be deleted
2. Adjust `older_than_days` in config (e.g., 30 days for monthly)
3. Execute deletion
4. Empty Gmail trash if desired

**Quarterly deep clean:**
1. Set `older_than_days` to 90 (3 months)
2. Run optimized deletion
3. Review and adjust rules based on results

## 📝 Example Workflow

### First-Time Setup
```bash
# 1. Set up project
git clone https://github.com/adrozdenko/gmail_bulk_delete.git
cd gmail_bulk_delete

# 2. Create Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Get credentials from Google Cloud Console
# (Follow Google Cloud Console steps above)

# 4. Test with dry-run
python gmail_bulk_delete.py

# 5. Review results and configure
# Edit delete_config.json as needed

# 6. Execute actual deletion
# Change dry_run to false and run again
```

### Regular Use
```bash
# Activate environment
source venv/bin/activate

# Quick cleanup
python gmail_bulk_delete.py

# Large volume cleanup
python delete_in_chunks.py
```

## 📞 Support

**Common Questions:**

**Q: Is this safe to use?**
A: Yes! The tool has multiple safety measures and only moves emails to trash (recoverable).

**Q: Will it delete my photos and documents?**
A: No! It specifically excludes emails with attachments.

**Q: Can I recover deleted emails?**
A: Yes! Emails are moved to Gmail trash, not permanently deleted.

**Q: How long does it take?**
A: Depends on volume. Small cleanups (hundreds): minutes. Large cleanups (thousands): can take an hour or more.

**Q: Does it work with G Suite/Google Workspace?**
A: Yes, but check with your administrator about API access policies.

**Q: Can I customize what gets deleted?**
A: Yes! Edit `delete_config.json` or create custom rules in `rules.json`.

## 🎉 Success Stories

**Typical results:**
- 📧 500-5,000+ emails cleaned up
- 💾 Significant storage space freed
- ⚡ Faster Gmail performance
- 🎯 Easier to find important emails
- 🗂️ Better organized inbox

**User feedback:**
- "Cleaned up 10,000+ old emails in one session!"
- "My Gmail is so much faster now"
- "Love that it kept all my photos safe"
- "Finally found emails that actually matter"

## 🚨 Important Notes

⚠️ **Always start with dry-run mode**  
⚠️ **Test with small batches first**  
⚠️ **Keep Gmail backup if you have critical emails**  
⚠️ **Internet connection required throughout process**  
⚠️ **Don't interrupt the process during large deletions**  

## 🎯 Ready to Start?

1. **Follow the Google Cloud Console setup** (most important step)
2. **Download and install the tool**
3. **Start with dry-run mode** to test safely
4. **Adjust configuration** based on preview
5. **Execute cleanup** when satisfied
6. **Enjoy your clean Gmail!**

---

*This tool was built following Emex development standards with safety, reliability, and user experience as top priorities.*