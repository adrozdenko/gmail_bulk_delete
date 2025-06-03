#!/usr/bin/env python3
"""High Performance Gmail Bulk Delete - Optimized for Maximum Speed"""

import pickle
import time
import asyncio
import aiohttp
import gc
import psutil
import os
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import threading

# Configuration Constants - Optimized for Async/Await
EMAILS_PER_CHUNK = 300  # Even larger chunks for async efficiency  
MAX_CONCURRENT_TASKS = 5  # Async concurrent tasks
EMAILS_PER_TASK = 60  # Emails per async task
MAX_RETRY_ATTEMPTS = 2
BACKOFF_BASE_DELAY = 0.05
STANDARD_DELAY = 0.05
ERROR_RECOVERY_DELAY = 0.5
MAINTENANCE_INTERVAL = 10
PERFORMANCE_CHECK_INTERVAL = 30
PROGRESS_BAR_WIDTH = 40

class AsyncGmailBulkDeleter:
    def __init__(self):
        self.total_deleted = 0
        self.total_errors = 0
        self.start_time = None
        self.lock = asyncio.Lock()
        self.rate_limit_counter = 0
        self.process = psutil.Process(os.getpid())
        self.batch_api_success = 0
        self.batch_api_fallbacks = 0
        
        # Service connection pooling for async
        self.service = None
        self.credentials = None
        self.connection_reuse_count = 0
        self._load_credentials()
        
    def get_memory_usage(self):
        """Get current memory usage in MB"""
        try:
            memory_info = self.process.memory_info()
            return memory_info.rss / 1024 / 1024  # Convert to MB
        except:
            return 0

    def _load_credentials(self):
        """Load credentials once for connection pooling"""
        with open('token.pickle', 'rb') as token:
            self.credentials = pickle.load(token)
        
    async def get_service(self):
        """Get Gmail service with async optimization"""
        if self.service is None:
            # Create service once for async use
            self.service = build('gmail', 'v1', 
                               credentials=self.credentials, 
                               cache_discovery=False)
        else:
            self.connection_reuse_count += 1
            
        return self.service

    async def delete_email_batch_async(self, message_ids, task_id):
        """Delete a batch of emails using async batch API for maximum performance"""
        service = await self.get_service()
        
        # Try batch API first (much faster)
        success = await self._delete_batch_api_async(service, message_ids)
        if success:
            deleted_count = len(message_ids)
            error_count = 0
            async with self.lock:
                self.batch_api_success += 1
        else:
            # Fallback to individual deletion if batch fails
            deleted_count, error_count = await self._delete_individual_fallback_async(service, message_ids)
            async with self.lock:
                self.batch_api_fallbacks += 1
                    
        await self._update_counters_async(deleted_count, error_count)
        return deleted_count, error_count

    async def _delete_batch_api_async(self, service, message_ids):
        """Delete emails using Gmail's batch API with async"""
        MAX_RETRIES = MAX_RETRY_ATTEMPTS
        
        for attempt in range(MAX_RETRIES):
            try:
                # Use batchModify to add TRASH label to all emails at once
                service.users().messages().batchModify(
                    userId='me',
                    body={
                        'ids': message_ids,
                        'addLabelIds': ['TRASH']
                    }
                ).execute()
                return True
            except HttpError as e:
                if self._is_rate_limit_error(e):
                    await self._handle_rate_limit_async()
                    if attempt < MAX_RETRIES - 1:
                        delay = self._calculate_backoff_delay(attempt)
                        await asyncio.sleep(delay)
                        continue
                # If not rate limit, fall back to individual deletion
                return False
            except Exception:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(0.1)
                    continue
                return False
        return False

    async def _delete_individual_fallback_async(self, service, message_ids):
        """Fallback to individual email deletion if batch API fails"""
        deleted_count = 0
        error_count = 0
        
        for message_id in message_ids:
            result = await self._delete_single_email_async(service, message_id)
            if result:
                deleted_count += 1
            else:
                error_count += 1
                
        return deleted_count, error_count

    async def _delete_single_email_async(self, service, message_id):
        """Delete a single email with async retry logic"""
        MAX_RETRIES = MAX_RETRY_ATTEMPTS
        
        for attempt in range(MAX_RETRIES):
            try:
                service.users().messages().trash(userId='me', id=message_id).execute()
                return True
            except HttpError as e:
                if self._is_rate_limit_error(e):
                    await self._handle_rate_limit_async()
                    if attempt < MAX_RETRIES - 1:
                        delay = self._calculate_backoff_delay(attempt)
                        await asyncio.sleep(delay)
                        continue
                return False
            except Exception:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(0.02)
                    continue
                return False
        return False

    def _is_rate_limit_error(self, error):
        """Check if error is rate limit related"""
        return "429" in str(error) or "403" in str(error)

    async def _handle_rate_limit_async(self):
        """Handle rate limit encounter with async"""
        async with self.lock:
            self.rate_limit_counter += 1

    def _calculate_backoff_delay(self, attempt):
        """Calculate progressive backoff delay"""
        return BACKOFF_BASE_DELAY * (attempt + 1) * min(self.rate_limit_counter, 5)

    async def _update_counters_async(self, deleted_count, error_count):
        """Update global counters with async lock"""
        async with self.lock:
            self.total_deleted += deleted_count
            self.total_errors += error_count

    async def execute_deletion_async(self):
        print("🚀 ASYNC HIGH PERFORMANCE GMAIL DELETION")
        print("⚡ Optimized with async/await for maximum speed")
        print("💾 Memory-optimized for minimal RAM usage")
        print("=" * 60)
        
        service = await self.get_service()
        query = 'before:2024/12/05 -is:important -is:starred -has:attachment -in:trash -in:spam'
        
        initial_estimate = await self._get_initial_email_count_async(service, query)
        
        print("\n⚡ MAXIMUM PERFORMANCE MODE:")
        print("   🚀 Batch API optimization enabled")
        print("   ⚡ Async/await concurrent processing")
        print("   🧵 5 concurrent async tasks")
        print("   📦 300 emails per chunk, 60 per task")
        print("   💾 Memory optimized")
        print("")
        
        self.start_time = datetime.now()
        batch_number = 1
        starting_total = initial_estimate
        
        # Maximum performance settings - async optimized
        CHUNK_SIZE = EMAILS_PER_CHUNK
        MAX_TASKS = MAX_CONCURRENT_TASKS  
        TASK_BATCH_SIZE = EMAILS_PER_TASK
        
        print(f"⚙️  Settings: {CHUNK_SIZE} emails/chunk, {MAX_TASKS} async tasks, {TASK_BATCH_SIZE} emails/task")
        print("=" * 60)
        
        last_performance_check = time.time()
        performance_samples = []
        
        while True:
            message_ids = await self._process_email_batch_async(service, query, CHUNK_SIZE)
            if not message_ids:
                break
                
            success = await self._process_batch_async(message_ids, batch_number, TASK_BATCH_SIZE, MAX_TASKS, performance_samples, starting_total, last_performance_check)
            
            batch_number += 1
            await self._perform_maintenance_async(batch_number)
            await self._apply_rate_limiting_async()

    async def _process_batch_async(self, message_ids, batch_number, task_batch_size, max_tasks, performance_samples, starting_total, last_performance_check):
        """Process a single batch of emails with async tasks"""
        try:
            chunk_start_time = time.time()
            
            print(f"\n📦 BATCH {batch_number}")
            print(f"   📧 Processing {len(message_ids)} emails with {max_tasks} async tasks...")
            
            task_batches = self._create_async_batches(message_ids, task_batch_size)
            await self._execute_async_deletion(task_batches, max_tasks)
            
            chunk_time = time.time() - chunk_start_time
            self._print_batch_stats(batch_number, len(message_ids), chunk_time, performance_samples)
            
            if self.rate_limit_counter > 0:
                print(f"   ⚠️  Rate limits hit: {self.rate_limit_counter} times")
                
            self._print_progress_bar(starting_total)
            self._print_periodic_status(last_performance_check)
            
            return True
        except Exception as e:
            print(f"\n💥 Error in batch {batch_number}: {e}")
            await asyncio.sleep(0.5)
            return False

    async def _perform_maintenance_async(self, batch_number):
        """Perform periodic maintenance with async"""
        if batch_number % 10 == 0:
            gc.collect()

    async def _apply_rate_limiting_async(self):
        """Apply rate limiting based on current conditions with async"""
        if self.rate_limit_counter > 0:
            delay = min(0.1 * (self.rate_limit_counter / 10), 1.0)
            await asyncio.sleep(delay)
        else:
            await asyncio.sleep(0.05)

    def _print_periodic_status(self, last_check_time):
        """Print periodic performance status"""
        current_time = time.time()
        if current_time - last_check_time > 30:
            total_time = current_time - self.start_time.timestamp()
            overall_rate = self.total_deleted / total_time if total_time > 0 else 0
            print(f"   📈 Performance: {overall_rate:.1f} emails/sec average")
            return current_time
        return last_check_time
        
        # Final results with extreme detail
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        final_rate = self.total_deleted / total_duration if total_duration > 0 else 0
        
        print("\n" + "=" * 60)
        print("🎉 HIGH PERFORMANCE DELETION COMPLETE!")
        print("=" * 60)
        print(f"📊 RESULTS:")
        print(f"   🗑️  Total deleted: {self.total_deleted}")
        print(f"   ❌ Total errors: {self.total_errors}")
        print(f"   ⏱️  Duration: {total_duration:.1f} seconds")
        print(f"   🚀 Average rate: {final_rate:.1f} emails/second")
        print(f"   ✅ Success rate: {(self.total_deleted/(self.total_deleted + self.total_errors)*100):.1f}%")
        print(f"   🚀 Batch API usage: {self.batch_api_success} successful, {self.batch_api_fallbacks} fallbacks")
        print(f"   🔗 Connection reuses: {self.connection_reuse_count}")
        if self.batch_api_success + self.batch_api_fallbacks > 0:
            batch_efficiency = (self.batch_api_success / (self.batch_api_success + self.batch_api_fallbacks)) * 100
            print(f"   📈 Batch API efficiency: {batch_efficiency:.1f}%")
        if self.connection_reuse_count > 1:
            print(f"   🔗 Connection pooling: ✅ Active ({self.connection_reuse_count} reuses)")
        
        return self.total_deleted

    async def _get_initial_email_count_async(self, service, query):
        """Get initial count of emails to delete with async"""
        print("📊 Analyzing emails...")
        try:
            result = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
            count = result.get('resultSizeEstimate', 0)
            print(f"📧 Initial estimate: {count} emails")
            return count
        except:
            return 0

    async def _process_email_batch_async(self, service, query, chunk_size):
        """Process a single batch of emails with async"""
        try:
            results = service.users().messages().list(
                userId='me', q=query, maxResults=chunk_size
            ).execute()
            
            messages = results.get('messages', [])
            if not messages:
                return None
                
            message_ids = [msg['id'] for msg in messages]
            del messages  # Free memory immediately
            return message_ids
        except Exception as e:
            print(f"\n💥 Error getting emails: {e}")
            return None

    def _create_async_batches(self, message_ids, batch_size):
        """Split message IDs into async task batches"""
        return [
            message_ids[i:i + batch_size] 
            for i in range(0, len(message_ids), batch_size)
        ]

    async def _execute_async_deletion(self, task_batches, max_tasks):
        """Execute deletion across multiple async tasks"""
        # Create tasks for concurrent execution
        tasks = []
        for i, batch in enumerate(task_batches):
            task = asyncio.create_task(self.delete_email_batch_async(batch, i))
            tasks.append(task)
        
        # Execute tasks concurrently with semaphore to limit concurrency
        semaphore = asyncio.Semaphore(max_tasks)
        
        async def bounded_task(task, task_id):
            async with semaphore:
                return await task
        
        # Run all tasks with concurrency control
        bounded_tasks = [bounded_task(task, i) for i, task in enumerate(tasks)]
        results = await asyncio.gather(*bounded_tasks, return_exceptions=True)
        
        # Print results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"   💥 Task {i} crashed: {result}")
            else:
                deleted, errors = result
                if errors > 0:
                    print(f"   🔧 Task {i}: {deleted} ✅, {errors} ❌")
                else:
                    print(f"   🔧 Task {i}: {deleted} ✅")

    def _get_initial_email_count(self, service, query):
        """Get initial count of emails to delete"""
        print("📊 Analyzing emails...")
        try:
            result = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
            count = result.get('resultSizeEstimate', 0)
            print(f"📧 Initial estimate: {count} emails")
            return count
        except:
            return 0

    def _process_email_batch(self, service, query, chunk_size):
        """Process a single batch of emails"""
        try:
            results = service.users().messages().list(
                userId='me', q=query, maxResults=chunk_size
            ).execute()
            
            messages = results.get('messages', [])
            if not messages:
                return None
                
            message_ids = [msg['id'] for msg in messages]
            del messages  # Free memory immediately
            return message_ids
        except Exception as e:
            print(f"\n💥 Error getting emails: {e}")
            return None

    def _create_thread_batches(self, message_ids, batch_size):
        """Split message IDs into thread batches"""
        return [
            message_ids[i:i + batch_size] 
            for i in range(0, len(message_ids), batch_size)
        ]

    def _execute_parallel_deletion(self, thread_batches, max_workers):
        """Execute deletion across multiple threads"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_thread = {
                executor.submit(self.delete_email_batch, batch, i): i 
                for i, batch in enumerate(thread_batches)
            }
            
            for future in concurrent.futures.as_completed(future_to_thread):
                thread_id = future_to_thread[future]
                try:
                    deleted, errors = future.result()
                    self._print_thread_result(thread_id, deleted, errors)
                except Exception as e:
                    print(f"   💥 Thread {thread_id} crashed: {e}")
        
        del thread_batches, future_to_thread

    def _print_thread_result(self, thread_id, deleted, errors):
        """Print result for a single thread"""
        if errors > 0:
            print(f"   🧵 Thread {thread_id}: {deleted} ✅, {errors} ❌")
        else:
            print(f"   🧵 Thread {thread_id}: {deleted} ✅")

    def _print_batch_stats(self, batch_num, email_count, chunk_time, performance_samples):
        """Print statistics for completed batch"""
        total_time = time.time() - self.start_time.timestamp()
        current_rate = email_count / chunk_time if chunk_time > 0 else 0
        overall_rate = self.total_deleted / total_time if total_time > 0 else 0
        
        performance_samples.append(current_rate)
        if len(performance_samples) > 10:
            performance_samples.pop(0)
            
        avg_recent_rate = sum(performance_samples) / len(performance_samples)
        
        print(f"   ⚡ Batch complete: {email_count} emails in {chunk_time:.1f}s")
        print(f"   🔥 Batch rate: {current_rate:.1f} emails/second")
        print(f"   📊 Overall rate: {overall_rate:.1f} emails/second")
        print(f"   📈 Recent avg: {avg_recent_rate:.1f} emails/second")
        print(f"   🎯 Total deleted: {self.total_deleted}")
        print(f"   💾 Memory: {self.get_memory_usage():.1f} MB")

    def _print_progress_bar(self, starting_total):
        """Print progress bar based on deletions"""
        if starting_total > 0:
            progress = min((self.total_deleted / starting_total) * 100, 100)
            bar_length = PROGRESS_BAR_WIDTH
            filled = int(bar_length * progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            estimated_remaining = max(0, starting_total - self.total_deleted)
            print(f"   📊 Progress: [{bar}] {progress:.1f}% (~{estimated_remaining} remaining)")
        else:
            print(f"   📊 Processed: {self.total_deleted} emails")

async def main_async():
    print("🚀 Gmail Bulk Delete - Async Maximum Performance")
    print("⚡ Deleting emails with async/await optimization")
    print()
    
    try:
        deleter = AsyncGmailBulkDeleter()
        await deleter.execute_deletion_async()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"\n\n💥 Error: {e}")

def main():
    """Main entry point that runs the async function"""
    asyncio.run(main_async())

if __name__ == "__main__":
    main()