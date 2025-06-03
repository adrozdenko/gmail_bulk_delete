#!/usr/bin/env python3
"""Delete emails in very small chunks to avoid timeouts"""

import pickle
import time
from googleapiclient.discovery import build

def delete_chunk():
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

    service = build('gmail', 'v1', credentials=creds)
    query = 'before:2024/12/05 -is:important -is:starred -has:attachment -in:trash -in:spam'

    try:
        # Get 20 emails
        results = service.users().messages().list(userId='me', q=query, maxResults=20).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print("✅ No more emails found!")
            return 0
        
        print(f"🗑️  Deleting {len(messages)} emails...")
        
        deleted = 0
        for message in messages:
            try:
                service.users().messages().trash(userId='me', id=message['id']).execute()
                deleted += 1
                print(f"  ✅ {deleted}/{len(messages)}")
            except Exception as e:
                print(f"  ❌ Error: {e}")
                continue
        
        print(f"✅ Chunk complete: {deleted} emails deleted")
        return deleted
    
    except Exception as e:
        print(f"❌ Chunk failed: {e}")
        return 0

# Run multiple chunks
total_deleted = 0
for chunk in range(1, 11):  # Up to 10 chunks (200 emails)
    print(f"\n📦 Chunk {chunk}:")
    deleted = delete_chunk()
    total_deleted += deleted
    
    if deleted == 0:
        break
    
    time.sleep(2)  # 2 second pause between chunks

print(f"\n🎉 TOTAL DELETED: {total_deleted} emails moved to trash!")