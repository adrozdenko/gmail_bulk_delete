#!/usr/bin/env python3
"""Display and user interface utilities"""

from typing import Dict, List
from constants import FILTER_PRESETS, DEFAULT_FILTERS, PROGRESS_BAR_WIDTH


class FilterDisplayHelper:
    """Helps display filter information and summaries"""
    
    @staticmethod
    def print_filter_summary(filters: Dict):
        """Print summary of active filters"""
        print("🎯 SMART FILTERING ACTIVE:")
        
        FilterDisplayHelper._print_age_filter(filters)
        FilterDisplayHelper._print_size_filter(filters)
        FilterDisplayHelper._print_sender_filters(filters)
        FilterDisplayHelper._print_subject_filter(filters)
        FilterDisplayHelper._print_exclusions(filters)
        print()
    
    @staticmethod
    def _print_age_filter(filters: Dict):
        """Print age filter information"""
        if filters.get("older_than_days"):
            print(f"   📅 Age: Older than {filters['older_than_days']} days")
    
    @staticmethod
    def _print_size_filter(filters: Dict):
        """Print size filter information"""
        min_size = filters.get("min_size_mb")
        max_size = filters.get("max_size_mb")
        
        if min_size or max_size:
            size_filter = "   📏 Size: "
            if min_size:
                size_filter += f"Larger than {min_size}MB"
            if max_size:
                if min_size:
                    size_filter += f", smaller than {max_size}MB"
                else:
                    size_filter += f"Smaller than {max_size}MB"
            print(size_filter)
    
    @staticmethod
    def _print_sender_filters(filters: Dict):
        """Print sender filter information"""
        domains = filters.get("sender_domains", [])
        emails = filters.get("sender_emails", [])
        
        if domains:
            print(f"   📧 Sender domains: {', '.join(domains)}")
        if emails:
            print(f"   📧 Sender emails: {', '.join(emails)}")
    
    @staticmethod
    def _print_subject_filter(filters: Dict):
        """Print subject filter information"""
        keywords = filters.get("subject_keywords", [])
        if keywords:
            print(f"   📝 Subject contains: {', '.join(keywords)}")
    
    @staticmethod
    def _print_exclusions(filters: Dict):
        """Print exclusion information"""
        exclusions = []
        if filters.get("exclude_attachments", True):
            exclusions.append("attachments")
        if filters.get("exclude_important", True):
            exclusions.append("important")
        if filters.get("exclude_starred", True):
            exclusions.append("starred")
        
        if exclusions:
            print(f"   🛡️  Excluding: {', '.join(exclusions)}")
        
        exclude_senders = filters.get("exclude_senders", [])
        if exclude_senders:
            print(f"   🚫 Never delete from: {', '.join(exclude_senders)}")


class ProgressDisplayHelper:
    """Helps display progress information"""
    
    @staticmethod
    def print_progress_bar(current: int, total: int):
        """Print progress bar"""
        if total <= 0:
            print(f"   📊 Processed: {current} emails")
            return
        
        progress = min((current / total) * 100, 100)
        filled = int(PROGRESS_BAR_WIDTH * progress / 100)
        bar = "█" * filled + "░" * (PROGRESS_BAR_WIDTH - filled)
        remaining = max(0, total - current)
        print(f"   📊 [{bar}] {progress:.1f}% (~{remaining} remaining)")
    
    @staticmethod
    def print_batch_stats(batch_num: int, email_count: int, 
                         duration: float, rate: float, 
                         total_deleted: int, memory_mb: float):
        """Print batch completion statistics"""
        print(f"   ⚡ Batch complete: {email_count} emails in {duration:.1f}s")
        print(f"   🔥 Batch rate: {rate:.1f} emails/second")
        print(f"   🎯 Total deleted: {total_deleted}")
        print(f"   💾 Memory: {memory_mb:.1f} MB")


class MenuHelper:
    """Helps display interactive menus"""
    
    @staticmethod
    def show_preset_menu() -> Dict:
        """Show filter preset selection menu"""
        print("🎯 SMART FILTERING PRESETS:")
        print("=" * 50)
        
        presets = {
            "1": ("default", "Default - 6 months old, preserve attachments"),
            "2": ("newsletters", "Newsletter cleanup - 30 days, newsletter keywords"),  
            "3": ("github_notifications", "GitHub notifications - 7 days old"),
            "4": ("large_emails", "Large emails - 90 days, 10MB+ size"),
            "5": ("social_media", "Social media - 14 days, FB/Twitter/LinkedIn"),
            "6": ("promotional", "Promotional emails - 60 days, sale keywords")
        }
        
        for key, (preset, desc) in presets.items():
            print(f"   {key}. {desc}")
        
        print("   7. Custom filters (advanced)")
        print()
        
        choice = input("Choose filter preset (1-7) or press Enter for default: ").strip()
        
        return MenuHelper._process_menu_choice(choice, presets)
    
    @staticmethod
    def _process_menu_choice(choice: str, presets: Dict) -> Dict:
        """Process user menu choice"""
        if choice == "1" or choice == "":
            return DEFAULT_FILTERS.copy()
        elif choice in ["2", "3", "4", "5", "6"]:
            preset_name = presets[choice][0]
            return FILTER_PRESETS[preset_name].copy()
        elif choice == "7":
            return MenuHelper._get_custom_filters()
        else:
            print("Invalid choice, using default filters")
            return DEFAULT_FILTERS.copy()
    
    @staticmethod
    def _get_custom_filters() -> Dict:
        """Get custom filter configuration from user"""
        print("\n🔧 CUSTOM FILTER CONFIGURATION:")
        print("=" * 40)
        
        filters = DEFAULT_FILTERS.copy()
        MenuHelper._configure_age_filter(filters)
        MenuHelper._configure_size_filters(filters)
        MenuHelper._configure_sender_filters(filters)
        MenuHelper._configure_subject_filter(filters)
        
        print("\n✅ Custom filters configured!")
        return filters
    
    @staticmethod
    def _configure_age_filter(filters: Dict):
        """Configure age filter"""
        current_days = filters['older_than_days']
        age_input = input(f"Delete emails older than days (current: {current_days}): ").strip()
        if age_input:
            try:
                filters['older_than_days'] = int(age_input)
            except ValueError:
                print("Invalid number, keeping current value")
    
    @staticmethod
    def _configure_size_filters(filters: Dict):
        """Configure size filters"""
        min_size = input("Minimum email size in MB (leave empty for no limit): ").strip()
        if min_size:
            try:
                filters['min_size_mb'] = int(min_size)
            except ValueError:
                print("Invalid number, ignoring")
        
        max_size = input("Maximum email size in MB (leave empty for no limit): ").strip()
        if max_size:
            try:
                filters['max_size_mb'] = int(max_size)
            except ValueError:
                print("Invalid number, ignoring")
    
    @staticmethod
    def _configure_sender_filters(filters: Dict):
        """Configure sender filters"""
        domains = input("Sender domains to delete (comma-separated, e.g., 'newsletter.com,marketing.com'): ").strip()
        if domains:
            filters['sender_domains'] = [d.strip() for d in domains.split(',')]
        
        emails = input("Specific sender emails to delete (comma-separated): ").strip()
        if emails:
            filters['sender_emails'] = [e.strip() for e in emails.split(',')]
    
    @staticmethod
    def _configure_subject_filter(filters: Dict):
        """Configure subject filter"""
        keywords = input("Subject keywords to match (comma-separated): ").strip()
        if keywords:
            filters['subject_keywords'] = [k.strip() for k in keywords.split(',')]