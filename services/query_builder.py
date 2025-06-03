#!/usr/bin/env python3
"""Gmail query builder for smart filtering"""

from datetime import datetime, timedelta
from typing import Dict, List
from constants import DATE_FORMAT


class QueryBuilder:
    """Builds Gmail search queries from filter configurations"""
    
    def __init__(self, filters: Dict):
        self.filters = filters
    
    def build_query(self) -> str:
        """Build complete Gmail search query"""
        query_parts = self._get_all_query_parts()
        return ' '.join(query_parts)
    
    def _get_all_query_parts(self) -> List[str]:
        """Get all query components"""
        parts = []
        parts.extend(self._build_date_filters())
        parts.extend(self._build_size_filters())
        parts.extend(self._build_sender_filters())
        parts.extend(self._build_subject_filters())
        parts.extend(self._build_exclusion_filters())
        return parts
    
    def _build_date_filters(self) -> List[str]:
        """Build date-based query parts"""
        parts = []
        if self.filters.get("older_than_days"):
            cutoff_date = self._calculate_cutoff_date()
            parts.append(f'before:{cutoff_date}')
        return parts
    
    def _calculate_cutoff_date(self) -> str:
        """Calculate cutoff date string"""
        days = self.filters["older_than_days"]
        cutoff_date = datetime.now() - timedelta(days=days)
        return cutoff_date.strftime(DATE_FORMAT)
    
    def _build_size_filters(self) -> List[str]:
        """Build size-based query parts"""
        parts = []
        if self.filters.get("min_size_mb"):
            parts.append(f'larger:{self.filters["min_size_mb"]}M')
        if self.filters.get("max_size_mb"):
            parts.append(f'smaller:{self.filters["max_size_mb"]}M')
        return parts
    
    def _build_sender_filters(self) -> List[str]:
        """Build sender-based query parts"""
        parts = []
        parts.extend(self._build_domain_filters())
        parts.extend(self._build_email_filters())
        return parts
    
    def _build_domain_filters(self) -> List[str]:
        """Build sender domain filters"""
        domains = self.filters.get("sender_domains", [])
        if not domains:
            return []
        
        domain_queries = [f'from:@{domain}' for domain in domains]
        return self._combine_or_queries(domain_queries)
    
    def _build_email_filters(self) -> List[str]:
        """Build sender email filters"""
        emails = self.filters.get("sender_emails", [])
        if not emails:
            return []
        
        email_queries = [f'from:{email}' for email in emails]
        return self._combine_or_queries(email_queries)
    
    def _build_subject_filters(self) -> List[str]:
        """Build subject keyword filters"""
        keywords = self.filters.get("subject_keywords", [])
        if not keywords:
            return []
        
        keyword_queries = [f'subject:"{keyword}"' for keyword in keywords]
        return self._combine_or_queries(keyword_queries)
    
    def _combine_or_queries(self, queries: List[str]) -> List[str]:
        """Combine multiple queries with OR logic"""
        if not queries:
            return []
        if len(queries) == 1:
            return queries
        return [f'({" OR ".join(queries)})']
    
    def _build_exclusion_filters(self) -> List[str]:
        """Build exclusion query parts"""
        parts = []
        parts.extend(self._build_standard_exclusions())
        parts.extend(self._build_sender_exclusions())
        parts.extend(self._build_label_exclusions())
        return parts
    
    def _build_standard_exclusions(self) -> List[str]:
        """Build standard exclusion filters"""
        parts = []
        if self.filters.get("exclude_attachments", True):
            parts.append('-has:attachment')
        if self.filters.get("exclude_important", True):
            parts.append('-is:important')
        if self.filters.get("exclude_starred", True):
            parts.append('-is:starred')
        return parts
    
    def _build_sender_exclusions(self) -> List[str]:
        """Build sender exclusion filters"""
        exclude_senders = self.filters.get("exclude_senders", [])
        return [f'-from:{sender}' for sender in exclude_senders]
    
    def _build_label_exclusions(self) -> List[str]:
        """Build label exclusion filters"""
        exclude_labels = self.filters.get("exclude_labels", [])
        return [f'-in:{label.lower()}' for label in exclude_labels]