#!/usr/bin/env python3
"""Gmail API client service"""

import pickle
from googleapiclient.discovery import build
from constants import GMAIL_API_VERSION, USER_ID


class GmailClient:
    """Manages Gmail API service connection"""
    
    def __init__(self):
        self.service = None
        self.credentials = None
        self.connection_reuse_count = 0
        self._load_credentials()
    
    def _load_credentials(self):
        """Load Gmail API credentials"""
        with open('token.pickle', 'rb') as token:
            self.credentials = pickle.load(token)
    
    async def get_service(self):
        """Get Gmail service with connection pooling"""
        if self.service is None:
            self.service = build('gmail', GMAIL_API_VERSION, 
                               credentials=self.credentials, 
                               cache_discovery=False)
        else:
            self.connection_reuse_count += 1
        return self.service
    
    async def get_initial_email_count(self, query: str) -> int:
        """Get estimated count of emails matching query"""
        try:
            service = await self.get_service()
            result = service.users().messages().list(
                userId=USER_ID, q=query, maxResults=1
            ).execute()
            return result.get('resultSizeEstimate', 0)
        except Exception:
            return 0
    
    async def get_email_batch(self, query: str, max_results: int) -> list:
        """Get batch of email IDs matching query"""
        try:
            service = await self.get_service()
            results = service.users().messages().list(
                userId=USER_ID, q=query, maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            if not messages:
                return []
            
            message_ids = [msg['id'] for msg in messages]
            del messages  # Free memory immediately
            return message_ids
        except Exception as e:
            print(f"Error getting emails: {e}")
            return []