#!/usr/bin/env python3
"""
Optimized Gmail Bulk Delete Script - Processes large volumes efficiently
"""

import os
import pickle
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scope for full access
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

@dataclass
class DeleteCriteria:
    """Configuration for email deletion criteria"""
    older_than_days: Optional[int] = None
    exclude_important: bool = True
    exclude_starred: bool = True
    exclude_with_attachments: bool = False
    dry_run: bool = True

class OptimizedGmailBulkDeleter:
    def __init__(self, credentials_file: str = 'credentials.json'):
        """Initialize Gmail API client"""
        self.credentials_file = credentials_file
        self.token_file = 'token.pickle'
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(f"Credentials file '{self.credentials_file}' not found.")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('gmail', 'v1', credentials=creds)
        print("✅ Successfully authenticated with Gmail API")
    
    def _build_query(self, criteria: DeleteCriteria) -> str:
        """Build Gmail search query from criteria"""
        query_parts = []
        
        if criteria.older_than_days:
            date = (datetime.now() - timedelta(days=criteria.older_than_days)).strftime('%Y/%m/%d')
            query_parts.append(f'before:{date}')
        
        if criteria.exclude_important:
            query_parts.append('-is:important')
        
        if criteria.exclude_starred:
            query_parts.append('-is:starred')
        
        if criteria.exclude_with_attachments:
            query_parts.append('-has:attachment')
        
        # Always exclude trash and spam
        query_parts.extend(['-in:trash', '-in:spam'])
        
        return ' '.join(query_parts)
    
    def count_matching_emails(self, criteria: DeleteCriteria) -> int:
        """Count total emails matching criteria without fetching all IDs"""
        query = self._build_query(criteria)
        print(f"🔍 Counting emails with query: {query}")
        
        # Use maxResults=1 just to get the total count estimate
        try:
            results = self.service.users().messages().list(
                userId='me', q=query, maxResults=1
            ).execute()
            
            # Get estimated total from Gmail
            if 'resultSizeEstimate' in results:
                return results['resultSizeEstimate']
            else:
                return len(results.get('messages', []))
                
        except HttpError as error:
            print(f"❌ Error counting emails: {error}")
            return 0
    
    def delete_emails_in_batches(self, criteria: DeleteCriteria, batch_size: int = 1000) -> int:
        """Delete emails in manageable batches"""
        query = self._build_query(criteria)
        print(f"🔍 Search query: {query}")
        
        total_deleted = 0
        batch_num = 1
        
        while True:
            print(f"\n📦 Processing batch {batch_num}...")
            
            # Get one batch of emails
            try:
                results = self.service.users().messages().list(
                    userId='me', q=query, maxResults=batch_size
                ).execute()
                
                messages = results.get('messages', [])
                
                if not messages:
                    print("✅ No more emails found!")
                    break
                
                batch_count = len(messages)
                print(f"📧 Found {batch_count} emails in this batch")
                
                if criteria.dry_run:
                    print(f"🧪 DRY RUN: Would delete {batch_count} emails")
                    total_deleted += batch_count
                else:
                    # Confirm each batch
                    response = input(f"\n⚠️  Delete {batch_count} emails in batch {batch_num}? (yes/no/all): ")
                    
                    if response.lower() == 'no':
                        print("❌ Batch cancelled")
                        break
                    elif response.lower() in ['yes', 'all']:
                        # Delete this batch
                        deleted_in_batch = self._delete_batch(messages)
                        total_deleted += deleted_in_batch
                        print(f"✅ Deleted {deleted_in_batch} emails from batch {batch_num}")
                        
                        if response.lower() == 'all':
                            # Continue without asking for subsequent batches
                            criteria.dry_run = False  # Ensure we're not in dry run
                            auto_confirm = True
                    else:
                        print("❌ Invalid response, skipping batch")
                        continue
                
                batch_num += 1
                
                # Rate limiting
                import time
                time.sleep(1)  # 1 second between batches
                
            except HttpError as error:
                print(f"❌ Error processing batch {batch_num}: {error}")
                break
        
        return total_deleted
    
    def _delete_batch(self, messages: List[Dict]) -> int:
        """Delete a batch of messages"""
        deleted_count = 0
        
        for message in messages:
            try:
                message_id = message['id']
                self.service.users().messages().trash(
                    userId='me', id=message_id
                ).execute()
                deleted_count += 1
                
                if deleted_count % 50 == 0:  # Progress update every 50 emails
                    print(f"  🗑️  Processed {deleted_count}/{len(messages)} emails...")
                    
            except HttpError as error:
                print(f"❌ Error deleting message {message_id}: {error}")
                continue
        
        return deleted_count

def load_config(config_file: str = 'delete_config.json') -> DeleteCriteria:
    """Load deletion criteria from config file"""
    if not os.path.exists(config_file):
        print(f"⚠️  Config file '{config_file}' not found. Using default criteria.")
        return DeleteCriteria()
    
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        return DeleteCriteria(**config_data)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return DeleteCriteria()

def main():
    """Main execution function"""
    try:
        # Load configuration
        criteria = load_config()
        
        # Initialize deleter
        deleter = OptimizedGmailBulkDeleter()
        
        print("🚀 Starting optimized Gmail bulk delete operation...")
        print(f"📊 Dry run mode: {'ON' if criteria.dry_run else 'OFF'}")
        
        # First, count total emails
        total_emails = deleter.count_matching_emails(criteria)
        print(f"📧 Estimated total emails matching criteria: {total_emails:,}")
        
        if total_emails == 0:
            print("✅ No emails found matching criteria")
            return
        
        if total_emails > 10000:
            print(f"⚠️  Large number of emails found ({total_emails:,})")
            response = input("This will take a while. Continue? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Operation cancelled")
                return
        
        # Delete in batches
        deleted_count = deleter.delete_emails_in_batches(criteria, batch_size=1000)
        
        print(f"\n🎯 Final result: {deleted_count:,} emails processed")
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")

if __name__ == "__main__":
    main()