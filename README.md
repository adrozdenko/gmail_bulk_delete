# Gmail Bulk Delete Tool

🚀 **Safe, powerful Gmail cleanup tool** that deletes old emails while protecting your important messages and attachments.

## ✨ What It Does

✅ **Safely deletes thousands of old emails** in minutes  
✅ **Preserves ALL emails with attachments** (photos, videos, documents)  
✅ **Keeps important and starred emails** completely safe  
✅ **Moves emails to trash** (recoverable, not permanent deletion)  
✅ **Works with any Gmail volume** - from hundreds to tens of thousands  

## 🎯 Perfect For

- 📧 **Cleaning up old newsletters and promotions**
- 💻 **Removing GitHub/development notifications** 
- 📱 **Deleting social media alerts**
- 📈 **Clearing marketing emails**
- 🗂️ **Organizing Gmail for better performance**
- 💾 **Freeing up Gmail storage space**

## ⚡ Quick Start

### 1. Easy Setup
```bash
# Download and setup
git clone https://github.com/adrozdenko/gmail_bulk_delete.git
cd gmail_bulk_delete

# Run automatic setup
./setup.sh        # macOS/Linux
# OR
setup.bat         # Windows
```

### 2. Get Gmail API Access
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create project → Enable Gmail API → Create OAuth credentials
- Download as `credentials.json` 
- **[Full instructions in USER_GUIDE.md](USER_GUIDE.md)**

### 3. Start Cleaning
```bash
# Safe test run (no deletion)
source venv/bin/activate
python gmail_bulk_delete.py

# Actual cleanup (when ready)
# Edit delete_config.json: change "dry_run" to false
python gmail_bulk_delete.py
```

## 📋 Real Results

**Typical cleanup achieves:**
- 🗑️ **500-5,000+ emails deleted** in one session
- 💾 **Significant storage freed** up
- ⚡ **Faster Gmail performance**  
- 🎯 **Easier to find important emails**
- 🛡️ **100% safety** - attachments and important emails preserved

## 🛡️ Safety Guarantees

### ✅ What's Protected (Never Deleted)
- **Emails with attachments** (photos, videos, documents)
- **Important emails** (marked important)
- **Starred emails** (your favorites)
- **Recent emails** (within your time limit)

### ✅ Safety Features
- **Dry-run mode by default** - test before real deletion
- **Preview shows exactly** what will be deleted
- **Emails moved to trash** - can be recovered
- **Batch processing** - handles large volumes safely
- **Smart exclusions** - multiple protection layers

## ⚙️ Easy Configuration

Edit `delete_config.json` to customize:

```json
{
  "older_than_days": 180,           // 6 months old
  "exclude_with_attachments": true, // Keep photos/videos/docs  
  "exclude_important": true,        // Keep important emails
  "exclude_starred": true,          // Keep starred emails
  "dry_run": true                   // Safe test mode
}
```

## 📊 Usage Options

### For Small Cleanup (< 1,000 emails)
```bash
python gmail_bulk_delete.py
```

### For Large Volumes (1,000+ emails)  
```bash
python delete_in_chunks.py
```

### Advanced CLI Interface
```bash
python -m src.main rules           # List cleanup rules
python -m src.main preview         # Safe preview
python -m src.main delete          # Execute cleanup
```

## 🎯 Built-in Cleanup Rules

| Rule | What It Cleans | Time Period |
|------|----------------|-------------|
| `keep_attachments_6months` | **Everything except attachments** | 6 months |
| `newsletter_cleanup` | **Newsletters and promotions** | 1 month |
| `large_emails_cleanup` | **Large files over 10MB** | 3 months |
| `social_cleanup` | **Social media notifications** | 2 months |

## 🚀 Complete Documentation

📖 **[USER_GUIDE.md](USER_GUIDE.md)** - Complete setup and usage guide  
🔧 **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical details and features  
📋 **[Configuration Examples](config.json.example)** - Sample configurations  

## 💡 Pro Tips

### First Time Users
1. **Always start with dry-run mode** (default)
2. **Review the preview** to see what will be deleted
3. **Start with small time periods** (30-90 days)
4. **Check Gmail trash** after deletion

### Power Users  
1. **Use chunk deletion** for large volumes
2. **Customize rules** in `rules.json`
3. **Set up regular schedules** (monthly/quarterly)
4. **Adjust batch sizes** for your internet speed

## 🔧 Requirements

- **Python 3.9+** (free from python.org)
- **Gmail account** 
- **Google Cloud Console access** (free)
- **5-10 minutes setup time**

## 📞 Troubleshooting

**Common issues and solutions:**

❓ **"Credentials file not found"**  
→ Download `credentials.json` from Google Cloud Console

❓ **"Access blocked during authorization"**  
→ Add your email as test user in OAuth consent screen

❓ **Tool times out with large volumes**  
→ Use `delete_in_chunks.py` for better performance

❓ **"Insufficient authentication scopes"**  
→ Ensure Gmail API scopes are properly configured

**[Full troubleshooting guide in USER_GUIDE.md](USER_GUIDE.md#-troubleshooting)**

## ⚠️ Important Notes

- **Emails are moved to trash** (not permanently deleted)
- **Always test with dry-run first**
- **Keep internet connection stable** during large operations
- **Review Gmail trash** before emptying permanently

## 🤝 Contributing

1. Fork the repository
2. Follow the [Emex development standards](https://github.com/Spilno-me/emex_dev_rules)
3. Submit pull requests with improvements

## 📝 License

MIT License - Use freely for personal and commercial projects.

---

### 🚀 Ready to Clean Up Your Gmail?

1. **[Read the complete setup guide](USER_GUIDE.md)**
2. **Download the tool and run setup**
3. **Get Gmail API credentials** 
4. **Start with a safe test run**
5. **Enjoy your organized Gmail!**

**Questions?** Check the [USER_GUIDE.md](USER_GUIDE.md) or open an issue.