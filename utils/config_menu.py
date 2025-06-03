#!/usr/bin/env python3
"""Configuration menu for JSON-based rule selection"""

import json
from typing import Dict, List
from services.config_loader import ConfigBasedFilter


class ConfigMenu:
    """Interactive menu for configuration selection"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_filter = ConfigBasedFilter(config_file)
    
    def show_preset_menu(self) -> Dict:
        """Show interactive preset selection menu"""
        print("🎯 JSON CONFIGURATION-BASED FILTERING:")
        print("=" * 55)
        
        presets = self.config_filter.get_available_presets()
        
        # Display presets with numbers
        preset_list = list(presets.items())
        for i, (name, description) in enumerate(preset_list, 1):
            print(f"   {i}. {name}: {description}")
        
        print(f"   {len(preset_list) + 1}. Custom rules (advanced)")
        print(f"   {len(preset_list) + 2}. Load from file")
        print()
        
        max_choice = len(preset_list) + 2
        choice = input(f"Choose option (1-{max_choice}) or press Enter for default: ").strip()
        
        return self._process_menu_choice(choice, preset_list)
    
    def _process_menu_choice(self, choice: str, preset_list: List) -> Dict:
        """Process user menu choice"""
        try:
            if choice == "" or choice == "1":
                # Default to first preset if available, otherwise default rules
                if preset_list:
                    return self.config_filter.create_filter_from_preset(preset_list[0][0])
                else:
                    return self._create_default_filter()
            
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(preset_list):
                preset_name = preset_list[choice_num - 1][0]
                return self.config_filter.create_filter_from_preset(preset_name)
            elif choice_num == len(preset_list) + 1:
                return self._get_custom_rules()
            elif choice_num == len(preset_list) + 2:
                return self._load_from_file()
            else:
                print("Invalid choice, using first preset")
                return self.config_filter.create_filter_from_preset(preset_list[0][0])
                
        except (ValueError, IndexError):
            print("Invalid choice, using first preset")
            if preset_list:
                return self.config_filter.create_filter_from_preset(preset_list[0][0])
            else:
                return self._create_default_filter()
    
    def _get_custom_rules(self) -> Dict:
        """Get custom rules from user input"""
        print("\n🔧 CUSTOM RULE CONFIGURATION:")
        print("=" * 40)
        print("Build your own rules step by step...")
        
        rules = []
        
        # Age rule
        self._add_age_rule(rules)
        self._add_sender_rules(rules)
        self._add_size_rules(rules)
        self._add_subject_rules(rules)
        self._add_exclusion_rules(rules)
        
        print(f"\n✅ Created {len(rules)} custom rules!")
        return self.config_filter.create_filter_from_rules(rules)
    
    def _add_age_rule(self, rules: List[Dict]):
        """Add age-based rule"""
        age_input = input("Delete emails older than how many days? (press Enter for 180): ").strip()
        days = 180  # default
        if age_input:
            try:
                days = int(age_input)
            except ValueError:
                print("Invalid number, using 180 days")
        rules.append({"type": "age", "days": days})
    
    def _add_sender_rules(self, rules: List[Dict]):
        """Add sender-based rules"""
        domains = input("Sender domains to target (comma-separated, e.g. 'newsletter.com,marketing.com'): ").strip()
        if domains:
            domain_list = [d.strip() for d in domains.split(',')]
            rules.append({"type": "sender", "domains": domain_list})
        
        emails = input("Specific sender emails to target (comma-separated): ").strip()
        if emails:
            email_list = [e.strip() for e in emails.split(',')]
            rules.append({"type": "sender", "emails": email_list})
    
    def _add_size_rules(self, rules: List[Dict]):
        """Add size-based rules"""
        min_size = input("Minimum email size in MB (leave empty for no limit): ").strip()
        max_size = input("Maximum email size in MB (leave empty for no limit): ").strip()
        
        size_rule = {"type": "size"}
        if min_size:
            try:
                size_rule["min_mb"] = int(min_size)
            except ValueError:
                print("Invalid minimum size, ignoring")
        
        if max_size:
            try:
                size_rule["max_mb"] = int(max_size)
            except ValueError:
                print("Invalid maximum size, ignoring")
        
        if len(size_rule) > 1:  # Has actual size constraints
            rules.append(size_rule)
    
    def _add_subject_rules(self, rules: List[Dict]):
        """Add subject-based rules"""
        keywords = input("Subject keywords to match (comma-separated): ").strip()
        if keywords:
            keyword_list = [k.strip() for k in keywords.split(',')]
            rules.append({"type": "subject", "keywords": keyword_list})
    
    def _add_exclusion_rules(self, rules: List[Dict]):
        """Add exclusion rules"""
        print("\nExclusion options (what to keep safe):")
        print("1. Exclude emails with attachments? (y/n): ", end="")
        if input().lower().startswith('y'):
            rules.append({"type": "exclude", "category": "attachments"})
        
        print("2. Exclude important emails? (y/n): ", end="")
        if input().lower().startswith('y'):
            rules.append({"type": "exclude", "category": "important"})
        
        print("3. Exclude starred emails? (y/n): ", end="")
        if input().lower().startswith('y'):
            rules.append({"type": "exclude", "category": "starred"})
        
        excluded_senders = input("4. Senders to never delete from (comma-separated): ").strip()
        if excluded_senders:
            sender_list = [s.strip() for s in excluded_senders.split(',')]
            rules.append({"type": "exclude", "senders": sender_list})
    
    def _load_from_file(self) -> Dict:
        """Load custom configuration from file"""
        filename = input("Enter configuration filename (e.g., 'my_config.json'): ").strip()
        if not filename:
            filename = "config.json"
        
        try:
            custom_filter = ConfigBasedFilter(filename)
            presets = custom_filter.get_available_presets()
            
            if not presets:
                print("No presets found in file, using default rules")
                return self._create_default_filter()
            
            print(f"Found {len(presets)} presets in {filename}:")
            preset_list = list(presets.items())
            for i, (name, desc) in enumerate(preset_list, 1):
                print(f"   {i}. {name}: {desc}")
            
            choice = input(f"Choose preset (1-{len(preset_list)}): ").strip()
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(preset_list):
                    preset_name = preset_list[choice_num - 1][0]
                    return custom_filter.create_filter_from_preset(preset_name)
            except ValueError:
                pass
            
            # Default to first preset
            return custom_filter.create_filter_from_preset(preset_list[0][0])
            
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            print("Using default configuration")
            return self._create_default_filter()
    
    def _create_default_filter(self) -> Dict:
        """Create a basic default filter"""
        default_rules = [
            {"type": "age", "days": 180},
            {"type": "exclude", "category": "attachments"},
            {"type": "exclude", "category": "important"},
            {"type": "exclude", "category": "starred"}
        ]
        return self.config_filter.create_filter_from_rules(default_rules)
    
    def print_filter_summary(self, filter_config: Dict):
        """Print summary of selected filter"""
        print("\n🎯 ACTIVE CONFIGURATION:")
        print("=" * 40)
        print(f"📝 Description: {filter_config['description']}")
        
        summary = filter_config['summary']
        
        if summary['age_days']:
            print(f"📅 Age: Older than {summary['age_days']} days")
        
        if summary['size_range']:
            size_info = "📏 Size: "
            if summary['size_range'].get('min_mb'):
                size_info += f"Larger than {summary['size_range']['min_mb']}MB"
            if summary['size_range'].get('max_mb'):
                if summary['size_range'].get('min_mb'):
                    size_info += f", smaller than {summary['size_range']['max_mb']}MB"
                else:
                    size_info += f"Smaller than {summary['size_range']['max_mb']}MB"
            print(size_info)
        
        if summary['sender_domains']:
            print(f"📧 Sender domains: {', '.join(summary['sender_domains'])}")
        
        if summary['sender_emails']:
            print(f"📧 Sender emails: {', '.join(summary['sender_emails'])}")
        
        if summary['subject_keywords']:
            print(f"📝 Subject keywords: {', '.join(summary['subject_keywords'])}")
        
        if summary['exclusions']:
            print(f"🛡️  Excluding: {', '.join(summary['exclusions'])}")
        
        if summary['excluded_senders']:
            print(f"🚫 Never delete from: {', '.join(summary['excluded_senders'])}")
        
        print(f"\n🔍 Gmail Query: {filter_config['query']}")
        print()