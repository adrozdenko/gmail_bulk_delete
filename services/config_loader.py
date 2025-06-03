#!/usr/bin/env python3
"""Configuration loader for rule-based Gmail deletion"""

import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
from constants import DATE_FORMAT


class ConfigLoader:
    """Loads and processes JSON configuration files"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file {self.config_file} not found")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {self.config_file}: {e}")
    
    def get_preset_names(self) -> List[str]:
        """Get list of available preset names"""
        return list(self.config.get("presets", {}).keys())
    
    def get_preset(self, preset_name: str) -> Dict:
        """Get preset configuration by name"""
        presets = self.config.get("presets", {})
        if preset_name not in presets:
            raise ValueError(f"Preset '{preset_name}' not found")
        return presets[preset_name]
    
    def get_default_rules(self) -> List[Dict]:
        """Get default rules from configuration"""
        return self.config.get("rules", [])
    
    def get_settings(self) -> Dict:
        """Get performance and behavior settings"""
        return self.config.get("settings", {})


class RuleProcessor:
    """Processes configuration rules into Gmail query components"""
    
    def __init__(self, rules: List[Dict]):
        self.rules = rules
    
    def build_gmail_query(self) -> str:
        """Build Gmail search query from rules"""
        query_parts = []
        
        for rule in self.rules:
            rule_type = rule.get("type")
            
            if rule_type == "age":
                query_parts.extend(self._process_age_rule(rule))
            elif rule_type == "size":
                query_parts.extend(self._process_size_rule(rule))
            elif rule_type == "sender":
                query_parts.extend(self._process_sender_rule(rule))
            elif rule_type == "subject":
                query_parts.extend(self._process_subject_rule(rule))
            elif rule_type == "exclude":
                query_parts.extend(self._process_exclude_rule(rule))
        
        return ' '.join(query_parts)
    
    def _process_age_rule(self, rule: Dict) -> List[str]:
        """Process age-based rule"""
        days = rule.get("days")
        if not days:
            return []
        
        cutoff_date = datetime.now() - timedelta(days=days)
        return [f'before:{cutoff_date.strftime(DATE_FORMAT)}']
    
    def _process_size_rule(self, rule: Dict) -> List[str]:
        """Process size-based rule"""
        parts = []
        
        min_mb = rule.get("min_mb")
        if min_mb:
            parts.append(f'larger:{min_mb}M')
        
        max_mb = rule.get("max_mb")
        if max_mb:
            parts.append(f'smaller:{max_mb}M')
        
        return parts
    
    def _process_sender_rule(self, rule: Dict) -> List[str]:
        """Process sender-based rule"""
        parts = []
        
        # Handle sender domains
        domains = rule.get("domains", [])
        if domains:
            domain_queries = [f'from:@{domain}' for domain in domains]
            if len(domain_queries) == 1:
                parts.append(domain_queries[0])
            else:
                parts.append(f'({" OR ".join(domain_queries)})')
        
        # Handle sender emails
        emails = rule.get("emails", [])
        if emails:
            email_queries = [f'from:{email}' for email in emails]
            if len(email_queries) == 1:
                parts.append(email_queries[0])
            else:
                parts.append(f'({" OR ".join(email_queries)})')
        
        return parts
    
    def _process_subject_rule(self, rule: Dict) -> List[str]:
        """Process subject-based rule"""
        keywords = rule.get("keywords", [])
        if not keywords:
            return []
        
        keyword_queries = [f'subject:"{keyword}"' for keyword in keywords]
        if len(keyword_queries) == 1:
            return keyword_queries
        else:
            return [f'({" OR ".join(keyword_queries)})']
    
    def _process_exclude_rule(self, rule: Dict) -> List[str]:
        """Process exclusion rule"""
        parts = []
        
        # Handle predefined categories
        category = rule.get("category")
        if category == "attachments":
            parts.append("-has:attachment")
        elif category == "important":
            parts.append("-is:important")
        elif category == "starred":
            parts.append("-is:starred")
        
        # Handle excluded senders
        senders = rule.get("senders", [])
        for sender in senders:
            parts.append(f'-from:{sender}')
        
        # Handle excluded labels
        labels = rule.get("labels", [])
        for label in labels:
            parts.append(f'-in:{label.lower()}')
        
        return parts
    
    def get_filter_summary(self) -> Dict[str, Any]:
        """Get human-readable summary of active filters"""
        summary = {
            "age_days": None,
            "size_range": {},
            "sender_domains": [],
            "sender_emails": [],
            "subject_keywords": [],
            "exclusions": [],
            "excluded_senders": []
        }
        
        for rule in self.rules:
            rule_type = rule.get("type")
            
            if rule_type == "age":
                summary["age_days"] = rule.get("days")
            elif rule_type == "size":
                if rule.get("min_mb"):
                    summary["size_range"]["min_mb"] = rule.get("min_mb")
                if rule.get("max_mb"):
                    summary["size_range"]["max_mb"] = rule.get("max_mb")
            elif rule_type == "sender":
                summary["sender_domains"].extend(rule.get("domains", []))
                summary["sender_emails"].extend(rule.get("emails", []))
            elif rule_type == "subject":
                summary["subject_keywords"].extend(rule.get("keywords", []))
            elif rule_type == "exclude":
                category = rule.get("category")
                if category:
                    summary["exclusions"].append(category)
                summary["excluded_senders"].extend(rule.get("senders", []))
        
        return summary


class ConfigBasedFilter:
    """Main interface for configuration-based filtering"""
    
    def __init__(self, config_file: str = "config.json"):
        self.loader = ConfigLoader(config_file)
    
    def get_available_presets(self) -> Dict[str, str]:
        """Get available presets with descriptions"""
        presets = {}
        for name in self.loader.get_preset_names():
            preset = self.loader.get_preset(name)
            presets[name] = preset.get("description", "No description")
        return presets
    
    def create_filter_from_preset(self, preset_name: str) -> Dict:
        """Create filter configuration from preset"""
        preset = self.loader.get_preset(preset_name)
        rules = preset.get("rules", [])
        
        processor = RuleProcessor(rules)
        
        return {
            "query": processor.build_gmail_query(),
            "summary": processor.get_filter_summary(),
            "rules": rules,
            "description": preset.get("description", "")
        }
    
    def create_filter_from_rules(self, rules: List[Dict]) -> Dict:
        """Create filter configuration from custom rules"""
        processor = RuleProcessor(rules)
        
        return {
            "query": processor.build_gmail_query(),
            "summary": processor.get_filter_summary(),
            "rules": rules,
            "description": "Custom configuration"
        }
    
    def get_performance_settings(self) -> Dict:
        """Get performance settings from configuration"""
        return self.loader.get_settings()