# Gmail Bulk Delete Tool

A secure, configurable Gmail bulk delete tool built following Emex development standards. Safely delete large numbers of emails based on flexible rules while preserving important messages and attachments.

## 🚀 Features

- **Rule-based filtering**: Predefined rules for common cleanup scenarios
- **Flexible configuration**: Custom search criteria and deletion parameters  
- **Safety-first design**: Dry-run mode, confirmation prompts, smart exclusions
- **Attachment preservation**: Automatically preserve emails with photos/videos/documents
- **Progress tracking**: Real-time progress with rich console output
- **Batch processing**: Efficient API usage with configurable batch sizes
- **Error handling**: Robust error recovery and detailed logging

## 📦 Installation

### Requirements
- Python 3.9+
- Gmail account with API access
- Google Cloud Console project

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/adrozdenko/gmail_bulk_delete.git
   cd gmail_bulk_delete
   ```

2. **Install dependencies**
   ```bash
   # Using Poetry (recommended)
   pip install poetry
   poetry install

   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up Gmail API credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create/select a project
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download as `credentials.json` and place in project root

## 🎯 Quick Start

### Using Predefined Rules

```bash
# List available rules
poetry run python -m src.main rules

# Preview what would be deleted (safe)
poetry run python -m src.main preview --rule keep_attachments_6months

# Execute deletion with rule
poetry run python -m src.main delete --rule keep_attachments_6months --no-dry-run
```

### Using Custom Configuration

```bash
# Generate default config file
poetry run python -m src.main config

# Edit config.json to your needs
# Then run deletion
poetry run python -m src.main delete
```

## 📋 Available Rules

| Rule Name | Description | Criteria |
|-----------|-------------|----------|
| `keep_attachments_6months` | Delete emails older than 6 months, preserve attachments | >180d, no attachments |
| `newsletter_cleanup` | Clean up newsletters and promotions | >30d, subjects: Newsletter, Unsubscribe, labels: promotions |
| `large_emails_cleanup` | Remove large emails older than 3 months | >90d, size: 10MB+ |
| `social_cleanup` | Clean up social media notifications | >60d, labels: social |

## ⚙️ Configuration

### Configuration File (`config.json`)

```json
{
  "search_criteria": {
    "older_than_days": 180,
    "exclude_with_attachments": true,
    "exclude_important": true,
    "exclude_starred": true,
    "from_addresses": ["newsletter@example.com"],
    "subject_contains": ["Unsubscribe"],
    "labels": ["promotions"],
    "size_larger_than_mb": 10
  },
  "dry_run": true,
  "batch_size": 100,
  "confirm_deletion": true
}
```

### Environment Variables

```bash
# Optional environment configuration
export GMAIL_DELETE_LOG_LEVEL=DEBUG
export GMAIL_DELETE_CREDENTIALS_FILE=my_credentials.json
export GMAIL_DELETE_DEFAULT_DRY_RUN=false
```

### Custom Rules (`rules.json`)

```json
{
  "my_custom_rule": {
    "description": "My custom cleanup rule",
    "criteria": {
      "older_than_days": 90,
      "from_addresses": ["noreply@example.com"],
      "exclude_important": true
    },
    "dry_run": true
  }
}
```

## 🛡️ Safety Features

- **Dry Run Mode**: Test operations without actual deletion
- **Smart Exclusions**: Never deletes important, starred, trash, or spam emails
- **Attachment Preservation**: Optionally preserve emails with attachments
- **Confirmation Prompts**: Require explicit confirmation before deletion
- **Progress Tracking**: Monitor operation progress with cancellation support
- **Error Recovery**: Continue operation even if individual batches fail

## 🚀 Usage Examples

### Basic Usage

```bash
# Safe preview (no deletion)
poetry run python -m src.main preview

# Execute with confirmation
poetry run python -m src.main delete --no-dry-run

# Use specific rule
poetry run python -m src.main delete --rule newsletter_cleanup
```

### Advanced Usage

```bash
# Custom configuration file
poetry run python -m src.main delete --config my_config.json

# Debug logging
poetry run python -m src.main --log-level DEBUG delete

# Log to file
poetry run python -m src.main --log-file cleanup.log delete
```

### Development Commands

```bash
# Code quality checks
make quality

# Auto-fix formatting
make quality-fix

# Run in development mode
make run-dry
```

## 📊 Project Structure

```
gmail_bulk_delete/
├── src/
│   ├── features/          # Feature-based architecture
│   │   ├── gmail_api/     # Gmail API integration
│   │   └── bulk_operations/  # Bulk delete operations
│   ├── config/            # Configuration management
│   ├── types/             # Type definitions
│   ├── utils/             # Shared utilities
│   └── main.py           # CLI entry point
├── pyproject.toml        # Project dependencies
├── Makefile             # Development commands
└── README.md            # This file
```

## 🔧 Development

### Setup Development Environment

```bash
# Install development dependencies
make dev-install

# Run quality checks
make quality

# Fix code formatting
make quality-fix
```

### Code Quality Standards

This project follows Emex development standards:
- **Feature-based architecture** (not type-based)
- **Max 40 lines per function**
- **Max 200 lines per file**
- **Strict typing** with mypy
- **Consistent formatting** with black/isort
- **Comprehensive linting** with flake8

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make changes following code quality standards
4. Run quality checks: `make quality`
5. Commit changes: `git commit -m 'feat: add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool permanently deletes emails. Always:
- Test with dry-run mode first
- Review preview results carefully
- Keep backups of important data
- Use at your own risk

## 🆘 Support

- 📖 [Documentation](./docs/)
- 🐛 [Report Issues](https://github.com/adrozdenko/gmail_bulk_delete/issues)
- 💬 [Discussions](https://github.com/adrozdenko/gmail_bulk_delete/discussions)