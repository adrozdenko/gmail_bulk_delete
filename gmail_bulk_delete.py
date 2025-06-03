#!/usr/bin/env python3
"""
Gmail Bulk Delete Script
A secure script to bulk delete emails using Gmail API with various filters.
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
    from_addresses: Optional[List[str]] = None
    subject_contains: Optional[List[str]] = None
    labels: Optional[List[str]] = None
    size_larger_than_mb: Optional[int] = None
    exclude_important: bool = True
    exclude_starred: bool = True
    exclude_with_attachments: bool = False
    dry_run: bool = True

class GmailBulkDeleter:
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
        
        # If credentials are invalid or don't exist, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file '{self.credentials_file}' not found. "
                        "Please download it from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
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
        
        if criteria.from_addresses:
            from_query = ' OR '.join([f'from:{addr}' for addr in criteria.from_addresses])
            query_parts.append(f'({from_query})')
        
        if criteria.subject_contains:
            subject_query = ' OR '.join([f'subject:"{text}"' for text in criteria.subject_contains])
            query_parts.append(f'({subject_query})')
        
        if criteria.labels:
            for label in criteria.labels:
                query_parts.append(f'label:{label}')
        
        if criteria.size_larger_than_mb:
            size_bytes = criteria.size_larger_than_mb * 1024 * 1024
            query_parts.append(f'size:{size_bytes}')
        
        if criteria.exclude_important:
            query_parts.append('-is:important')
        
        if criteria.exclude_starred:
            query_parts.append('-is:starred')
        
        # Always exclude trash and spam
        query_parts.extend(['-in:trash', '-in:spam'])
        
        # Exclude emails with attachments if specified
        if criteria.exclude_with_attachments:
            query_parts.append('-has:attachment')
        
        return ' '.join(query_parts)
    
    def search_emails(self, criteria: DeleteCriteria) -> List[Dict]:
        """Search for emails matching criteria"""
        query = self._build_query(criteria)
        print(f"🔍 Search query: {query}")
        
        try:
            # Get ALL messages with pagination
            messages = []
            page_token = None
            
            while True:
                if page_token:
                    results = self.service.users().messages().list(
                        userId='me', q=query, pageToken=page_token
                    ).execute()
                else:
                    results = self.service.users().messages().list(
                        userId='me', q=query
                    ).execute()
                
                batch_messages = results.get('messages', [])
                messages.extend(batch_messages)
                
                page_token = results.get('nextPageToken')
                if not page_token:
                    break
                    
                print(f"📧 Found {len(messages)} emails so far...")
            
            total_count = len(messages)
            
            if total_count == 0:
                print("✅ No emails found matching criteria")
                return []
            
            print(f"📧 Found {total_count} emails matching criteria")
            
            # Get detailed info for first few emails as preview
            preview_emails = []
            for i, message in enumerate(messages[:5]):  # Preview first 5
                try:
                    email_data = self.service.users().messages().get(
                        userId='me', id=message['id'], format='metadata',
                        metadataHeaders=['From', 'Subject', 'Date']
                    ).execute()
                    
                    headers = {h['name']: h['value'] for h in email_data['payload'].get('headers', [])}
                    preview_emails.append({
                        'id': message['id'],
                        'from': headers.get('From', 'Unknown'),
                        'subject': headers.get('Subject', 'No Subject'),
                        'date': headers.get('Date', 'Unknown')
                    })
                except HttpError as e:
                    print(f"⚠️  Error getting email details: {e}")
            
            if preview_emails:
                print("\n📋 Preview of emails to be deleted:")
                for email in preview_emails:
                    print(f"  • From: {email['from']}")
                    print(f"    Subject: {email['subject']}")
                    print(f"    Date: {email['date']}")
                    print()
                
                if total_count > 5:
                    print(f"... and {total_count - 5} more emails")
            
            return messages
            
        except HttpError as error:
            print(f"❌ Error searching emails: {error}")
            return []
    
    def delete_emails(self, message_ids: List[str], dry_run: bool = True) -> int:
        """Delete emails by ID"""
        if not message_ids:
            return 0
        
        total_count = len(message_ids)
        
        if dry_run:
            print(f"🧪 DRY RUN: Would delete {total_count} emails")
            return 0
        
        print(f"🗑️  Deleting {total_count} emails...")
        
        # Confirm deletion
        response = input(f"\n⚠️  Are you sure you want to delete {total_count} emails? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Deletion cancelled")
            return 0
        
        deleted_count = 0
        batch_size = 100  # Gmail API batch limit
        
        try:
            for i in range(0, len(message_ids), batch_size):
                batch = message_ids[i:i + batch_size]
                
                # Move to trash instead of permanent deletion (safer and works with current permissions)
                for message_id in batch:
                    self.service.users().messages().trash(
                        userId='me', id=message_id
                    ).execute()
                
                deleted_count += len(batch)
                print(f"✅ Deleted {deleted_count}/{total_count} emails")
            
            print(f"🎉 Successfully deleted {deleted_count} emails!")
            return deleted_count
            
        except HttpError as error:
            print(f"❌ Error deleting emails: {error}")
            return deleted_count
    
    def bulk_delete(self, criteria: DeleteCriteria) -> int:
        """Main method to search and delete emails"""
        print("🚀 Starting Gmail bulk delete operation...")
        print(f"📊 Dry run mode: {'ON' if criteria.dry_run else 'OFF'}")
        
        # Search for emails
        messages = self.search_emails(criteria)
        
        if not messages:
            return 0
        
        # Extract message IDs
        message_ids = [msg['id'] for msg in messages]
        
        # Delete emails
        return self.delete_emails(message_ids, criteria.dry_run)

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
        print("Using default criteria.")
        return DeleteCriteria()

def main():
    """Main execution function"""
    try:
        # Load configuration
        criteria = load_config()
        
        # Initialize deleter
        deleter = GmailBulkDeleter()
        
        # Perform bulk delete
        deleted_count = deleter.bulk_delete(criteria)
        
        if deleted_count > 0:
            print(f"\n🎯 Final result: {deleted_count} emails deleted")
        else:
            print("\n💡 No emails were deleted")
    
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")

if __name__ == "__main__":
    main()