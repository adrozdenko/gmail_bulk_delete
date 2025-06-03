#!/usr/bin/env python3
"""Quick delete remaining emails in small fast batches"""

import pickle
from googleapiclient.discovery import build

# Load existing authentication
with open('token.pickle', 'rb') as token:
    creds = pickle.load(token)

service = build('gmail', 'v1', credentials=creds)

# Quick deletion in small batches
query = 'before:2024/12/05 -is:important -is:starred -has:attachment -in:trash -in:spam'

print("🚀 Quick deletion of remaining emails...")

total_deleted = 0
batch_size = 50  # Smaller batches for faster processing

for batch_num in range(1, 10):  # Max 10 batches (500 emails)
    try:
        # Get small batch
        results = service.users().messages().list(
            userId='me', q=query, maxResults=batch_size
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            print(f"✅ All done! No more emails found.")
            break
        
        print(f"📦 Batch {batch_num}: Deleting {len(messages)} emails...")
        
        # Delete quickly
        for message in messages:
            try:
                service.users().messages().trash(
                    userId='me', id=message['id']
                ).execute()
                total_deleted += 1
            except:
                continue
        
        print(f"✅ Batch {batch_num} done: {total_deleted} total deleted")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        break

print(f"🎉 QUICK DELETION COMPLETE: {total_deleted} emails moved to trash!")