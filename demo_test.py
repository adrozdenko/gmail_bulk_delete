#!/usr/bin/env python3
"""Demo test to show the tool functionality without Gmail credentials."""

import json
from src.config import ConfigManager
from src.types import GmailSearchQuery


def demo_configuration_system():
    """Demonstrate the configuration and rules system."""
    print("🎯 Gmail Bulk Delete Tool - Demo Test")
    print("=" * 50)
    
    # Initialize config manager
    config_manager = ConfigManager()
    
    # Test 1: Show available rules
    print("\n1. 📋 Available Rules:")
    rules = config_manager.list_available_rules()
    rules_data = config_manager.load_rules()
    
    for rule_name in rules:
        rule_info = rules_data[rule_name]
        print(f"   • {rule_name}: {rule_info['description']}")
    
    # Test 2: Generate config from your main rule
    print("\n2. ⚙️ Your Main Rule Configuration:")
    config = config_manager.create_config_from_rules("keep_attachments_6months")
    
    print(f"   Dry Run: {config.dry_run}")
    print(f"   Batch Size: {config.batch_size}")
    print("\n   Search Criteria:")
    criteria = config.search_criteria
    print(f"   - Older than: {criteria.older_than_days} days")
    print(f"   - Exclude attachments: {criteria.exclude_with_attachments}")
    print(f"   - Exclude important: {criteria.exclude_important}")
    print(f"   - Exclude starred: {criteria.exclude_starred}")
    
    # Test 3: Show what Gmail query would be built
    print("\n3. 🔍 Gmail Search Query (what would be sent to Gmail API):")
    query_parts = []
    
    if criteria.older_than_days:
        from datetime import datetime, timedelta
        cutoff_date = (datetime.now() - timedelta(days=criteria.older_than_days)).strftime('%Y/%m/%d')
        query_parts.append(f"before:{cutoff_date}")
    
    if criteria.exclude_important:
        query_parts.append("-is:important")
    
    if criteria.exclude_starred:
        query_parts.append("-is:starred")
    
    if criteria.exclude_with_attachments:
        query_parts.append("-has:attachment")
    
    query_parts.extend(["-in:trash", "-in:spam"])
    
    query_string = " ".join(query_parts)
    print(f"   Gmail Query: '{query_string}'")
    
    # Test 4: Show configuration flexibility
    print("\n4. 🔧 Configuration Flexibility:")
    print("   You can modify rules by creating custom rules.json:")
    
    custom_rule = {
        "my_custom_rule": {
            "description": "Delete old newsletters but keep everything else",
            "criteria": {
                "older_than_days": 90,
                "subject_contains": ["Newsletter", "Unsubscribe"],
                "exclude_important": True,
                "exclude_starred": True,
                "exclude_with_attachments": True
            },
            "dry_run": True
        }
    }
    
    print("   Example custom rule:")
    print(json.dumps(custom_rule, indent=4))
    
    print("\n✅ Demo completed successfully!")
    print("\n📋 Next Steps:")
    print("   1. Get Gmail API credentials from Google Cloud Console")
    print("   2. Run: python -m src.main preview --rule keep_attachments_6months")
    print("   3. If satisfied: python -m src.main delete --rule keep_attachments_6months --no-dry-run")


if __name__ == "__main__":
    demo_configuration_system()