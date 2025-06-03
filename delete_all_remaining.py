#!/usr/bin/env python3
"""Delete all remaining emails matching criteria"""

from gmail_bulk_delete_optimized import OptimizedGmailBulkDeleter, load_config

def delete_all_remaining():
    # Load config
    criteria = load_config()
    criteria.dry_run = False  # Disable dry run
    
    deleter = OptimizedGmailBulkDeleter()
    
    print("🚀 Deleting ALL remaining emails older than 6 months (excluding attachments)...")
    
    total_deleted = 0
    batch_num = 1
    
    while True:
        query = deleter._build_query(criteria)
        
        # Get emails
        try:
            results = deleter.service.users().messages().list(
                userId='me', q=query, maxResults=100
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print(f"✅ All done! No more emails found.")
                break
            
            print(f"📦 Batch {batch_num}: Processing {len(messages)} emails...")
            
            # Delete this batch
            deleted_in_batch = 0
            for i, message in enumerate(messages):
                try:
                    message_id = message['id']
                    deleter.service.users().messages().trash(
                        userId='me', id=message_id
                    ).execute()
                    deleted_in_batch += 1
                    
                    if (i + 1) % 20 == 0:  # Progress every 20 emails
                        print(f"  🗑️  Processed {i + 1}/{len(messages)} emails...")
                        
                except Exception as e:
                    print(f"  ❌ Error with email {i+1}: {e}")
                    continue
            
            total_deleted += deleted_in_batch
            print(f"✅ Batch {batch_num} complete: {deleted_in_batch} emails moved to trash")
            print(f"📊 Total deleted so far: {total_deleted}")
            
            batch_num += 1
            
            # Small delay between batches
            import time
            time.sleep(0.5)
            
        except Exception as error:
            print(f"❌ Error in batch {batch_num}: {error}")
            break
    
    print(f"🎉 FINAL RESULT: {total_deleted} emails moved to trash!")
    return total_deleted

if __name__ == "__main__":
    delete_all_remaining()