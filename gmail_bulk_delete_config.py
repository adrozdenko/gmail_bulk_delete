#!/usr/bin/env python3
"""Gmail Bulk Delete - JSON Configuration-Based Version"""

import asyncio
from services.deletion_orchestrator import DeletionOrchestrator
from utils.config_menu import ConfigMenu


class ConfigBasedDeletionOrchestrator(DeletionOrchestrator):
    """Extended orchestrator that uses JSON configuration"""
    
    def __init__(self, filter_config: dict):
        # Convert config format to old filter format for compatibility
        self.filter_config = filter_config
        legacy_filters = self._convert_to_legacy_format(filter_config)
        super().__init__(legacy_filters)
    
    def _convert_to_legacy_format(self, config: dict) -> dict:
        """Convert new config format to legacy filter format"""
        summary = config['summary']
        
        legacy = {
            "older_than_days": summary.get('age_days'),
            "exclude_attachments": 'attachments' in summary.get('exclusions', []),
            "exclude_important": 'important' in summary.get('exclusions', []),
            "exclude_starred": 'starred' in summary.get('exclusions', []),
            "sender_domains": summary.get('sender_domains', []),
            "sender_emails": summary.get('sender_emails', []),
            "subject_keywords": summary.get('subject_keywords', []),
            "exclude_senders": summary.get('excluded_senders', []),
            "exclude_labels": ["TRASH", "SPAM"]
        }
        
        # Handle size filters
        size_range = summary.get('size_range', {})
        legacy["min_size_mb"] = size_range.get('min_mb')
        legacy["max_size_mb"] = size_range.get('max_mb')
        
        return legacy
    
    def _print_query_info(self, query: str):
        """Override to show config-based information"""
        print(f"📧 Gmail Query: {query}")
        print()
        
        # Use the config menu's summary printer
        menu = ConfigMenu()
        menu.print_filter_summary(self.filter_config)


async def main_async():
    """Main async entry point with JSON configuration"""
    print("🚀 Gmail Bulk Delete - JSON Configuration System")
    print("⚡ Rule-based filtering with preset configurations")
    print()
    
    # Get configuration from user
    menu = ConfigMenu()
    filter_config = menu.show_preset_menu()
    
    try:
        orchestrator = ConfigBasedDeletionOrchestrator(filter_config)
        result = await orchestrator.execute_deletion()
        return result
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
        return None
    except Exception as e:
        print(f"\n\n💥 Error: {e}")
        return None


def main():
    """Main entry point"""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()