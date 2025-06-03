#!/usr/bin/env python3
"""High Performance Gmail Bulk Delete - Optimized for Maximum Speed"""

import pickle
import time
import concurrent.futures
import threading
import gc
import psutil
import os
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class HighPerformanceDeleter:
    def __init__(self):
        self.total_deleted = 0
        self.total_errors = 0
        self.start_time = None
        self.lock = threading.Lock()
        self.rate_limit_counter = 0
        self.process = psutil.Process(os.getpid())
        
    def get_memory_usage(self):
        """Get current memory usage in MB"""
        try:
            memory_info = self.process.memory_info()
            return memory_info.rss / 1024 / 1024  # Convert to MB
        except:
            return 0
        
    def load_service(self):
        """Load Gmail service for this thread with memory optimization"""
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        # Use cache_discovery=False to reduce memory usage
        return build('gmail', 'v1', credentials=creds, cache_discovery=False)

    def delete_email_batch_aggressive(self, message_ids, thread_id):
        """Delete a batch of emails with aggressive optimization"""
        service = self.load_service()
        thread_deleted = 0
        thread_errors = 0
        
        for message_id in message_ids:
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    service.users().messages().trash(userId='me', id=message_id).execute()
                    thread_deleted += 1
                    break
                except HttpError as e:
                    if "429" in str(e) or "403" in str(e):  # Rate limit or quota
                        with self.lock:
                            self.rate_limit_counter += 1
                        if attempt < max_retries - 1:
                            # Progressive backoff: start small, increase if needed
                            delay = 0.05 * (attempt + 1) * min(self.rate_limit_counter, 5)
                            time.sleep(delay)
                        else:
                            thread_errors += 1
                    else:
                        thread_errors += 1
                        break
                except Exception:
                    if attempt < max_retries - 1:
                        time.sleep(0.02)  # Tiny delay for other errors
                    else:
                        thread_errors += 1
                    
        # Update global counters thread-safely
        with self.lock:
            self.total_deleted += thread_deleted
            self.total_errors += thread_errors
            
        return thread_deleted, thread_errors

    def high_performance_delete(self):
        print("🚀 HIGH PERFORMANCE GMAIL DELETION")
        print("⚡ Optimized for maximum speed and efficiency")
        print("💾 Memory-optimized for minimal RAM usage")
        print("=" * 60)
        
        service = self.load_service()
        query = 'before:2024/12/05 -is:important -is:starred -has:attachment -in:trash -in:spam'
        
        # Get initial count
        print("📊 Analyzing emails...")
        try:
            count_result = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
            initial_estimate = count_result.get('resultSizeEstimate', 0)
            print(f"📧 Initial estimate: {initial_estimate} emails")
        except:
            initial_estimate = 0
        
        print("\n⚡ HIGH PERFORMANCE OPTIMIZATIONS:")
        print("   🧵 Parallel processing (5 threads)")
        print("   📦 Large batch sizes (100 emails/chunk)")
        print("   🎯 Optimized thread distribution (10 emails/thread)")
        print("   ⏱️  Minimal delays for maximum speed")
        print("   🔄 Smart rate limit handling")
        print("   📈 Real-time performance monitoring")
        print("   💾 Memory optimization (garbage collection, cache_discovery=False)")
        print("   🔧 Efficient data structures and cleanup")
        print("")
        
        self.start_time = datetime.now()
        batch_number = 1
        starting_total = initial_estimate
        
        # EXTREME Performance settings
        CHUNK_SIZE = 100  # Maximum chunk size
        MAX_WORKERS = 5   # Maximum threads
        THREAD_BATCH_SIZE = 10  # More emails per thread
        
        print(f"⚙️  Settings: {CHUNK_SIZE} emails/chunk, {MAX_WORKERS} threads, {THREAD_BATCH_SIZE} emails/thread")
        print("=" * 60)
        
        last_performance_check = time.time()
        performance_samples = []
        
        while True:
            try:
                # Get maximum chunk of emails
                results = service.users().messages().list(
                    userId='me', q=query, maxResults=CHUNK_SIZE
                ).execute()
                
                messages = results.get('messages', [])
                if not messages:
                    break
                
                # Extract only message IDs to minimize memory usage
                message_ids = [msg['id'] for msg in messages]
                chunk_start_time = time.time()
                
                # Clear messages list to free memory immediately
                del messages
                
                print(f"\n📦 BATCH {batch_number}")
                print(f"   📧 Processing {len(message_ids)} emails with {MAX_WORKERS} threads...")
                
                # Split emails into thread batches efficiently
                thread_batches = [
                    message_ids[i:i + THREAD_BATCH_SIZE] 
                    for i in range(0, len(message_ids), THREAD_BATCH_SIZE)
                ]
                
                # Process in parallel with maximum aggression
                with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_to_thread = {
                        executor.submit(self.delete_email_batch_aggressive, batch, i): i 
                        for i, batch in enumerate(thread_batches)
                    }
                    
                    # Monitor progress with detailed metrics
                    completed_threads = 0
                    for future in concurrent.futures.as_completed(future_to_thread):
                        thread_id = future_to_thread[future]
                        try:
                            thread_deleted, thread_errors = future.result()
                            completed_threads += 1
                            if thread_errors > 0:
                                print(f"   🧵 Thread {thread_id}: {thread_deleted} ✅, {thread_errors} ❌")
                            else:
                                print(f"   🧵 Thread {thread_id}: {thread_deleted} ✅")
                        except Exception as e:
                            print(f"   💥 Thread {thread_id} crashed: {e}")
                
                # Clear thread batches and futures to free memory
                del thread_batches, future_to_thread
                
                # Calculate advanced performance metrics
                chunk_time = time.time() - chunk_start_time
                total_time = time.time() - self.start_time.timestamp()
                current_rate = len(message_ids) / chunk_time if chunk_time > 0 else 0
                overall_rate = self.total_deleted / total_time if total_time > 0 else 0
                
                # Track performance samples for trending
                performance_samples.append(current_rate)
                if len(performance_samples) > 10:
                    performance_samples.pop(0)
                
                avg_recent_rate = sum(performance_samples) / len(performance_samples)
                
                print(f"   ⚡ Batch complete: {len(message_ids)} emails in {chunk_time:.1f}s")
                print(f"   🔥 Batch rate: {current_rate:.1f} emails/second")
                print(f"   📊 Overall rate: {overall_rate:.1f} emails/second")
                print(f"   📈 Recent avg: {avg_recent_rate:.1f} emails/second")
                print(f"   🎯 Total deleted: {self.total_deleted}")
                
                # Memory usage monitoring
                current_memory = self.get_memory_usage()
                print(f"   💾 Memory: {current_memory:.1f} MB")
                
                # Rate limit monitoring
                if self.rate_limit_counter > 0:
                    print(f"   ⚠️  Rate limits hit: {self.rate_limit_counter} times")
                
                # Progress bar based on deletions vs initial estimate
                if starting_total > 0:
                    progress = min((self.total_deleted / starting_total) * 100, 100)
                    bar_length = 40
                    filled = int(bar_length * progress / 100)
                    bar = "█" * filled + "░" * (bar_length - filled)
                    estimated_remaining = max(0, starting_total - self.total_deleted)
                    print(f"   📊 Progress: [{bar}] {progress:.1f}% (~{estimated_remaining} remaining)")
                else:
                    print(f"   📊 Processed: {self.total_deleted} emails")
                
                # Performance monitoring and adaptation  
                current_time = time.time()
                if current_time - last_performance_check > 30:  # Every 30 seconds
                    try:
                        # Update remaining count for trending
                        trend_check = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
                        current_remaining = trend_check.get('resultSizeEstimate', 0)
                        print(f"   📈 Performance trending: {overall_rate:.1f} emails/sec average, {current_remaining} remaining")
                        if self.rate_limit_counter > 10:
                            print(f"   ⚠️  High rate limit pressure detected - consider reducing threads")
                    except:
                        print(f"   📈 Performance trending: {overall_rate:.1f} emails/sec average")
                    last_performance_check = current_time
                
                batch_number += 1
                
                # Memory cleanup every 10 batches
                if batch_number % 10 == 0:
                    gc.collect()  # Force garbage collection
                
                # Minimal delay - only if we're hitting rate limits
                if self.rate_limit_counter > 0:
                    adaptive_delay = min(0.1 * (self.rate_limit_counter / 10), 1.0)
                    time.sleep(adaptive_delay)
                else:
                    time.sleep(0.05)  # Minimal pause
                
            except Exception as e:
                print(f"\n💥 Error in batch {batch_number}: {e}")
                time.sleep(0.5)  # Quick recovery
                batch_number += 1
                continue
        
        # Final results with extreme detail
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        final_rate = self.total_deleted / total_duration if total_duration > 0 else 0
        
        print("\n" + "=" * 60)
        print("🎉 HIGH PERFORMANCE DELETION COMPLETE!")
        print("=" * 60)
        print(f"📊 PERFORMANCE RESULTS:")
        print(f"   🗑️  Total deleted: {self.total_deleted}")
        print(f"   ❌ Total errors: {self.total_errors}")
        print(f"   ⏱️  Duration: {total_duration:.1f} seconds")
        print(f"   🚀 Average rate: {final_rate:.1f} emails/second")
        print(f"   📈 Improvement vs baseline: {final_rate/1.9:.1f}x faster")
        print(f"   📈 Improvement vs optimized: {final_rate/4.6:.1f}x faster")
        print(f"   ✅ Success rate: {(self.total_deleted/(self.total_deleted + self.total_errors)*100):.1f}%")
        print(f"   ⚠️  Rate limit encounters: {self.rate_limit_counter}")
        
        # Performance analysis
        print(f"\n🔬 PERFORMANCE ANALYSIS:")
        if final_rate > 6.0:
            print(f"   🎉 EXCELLENT: Achieved {final_rate:.1f} emails/sec (30% improvement!)")
        elif final_rate > 5.0:
            print(f"   ✅ GOOD: Achieved {final_rate:.1f} emails/sec (modest improvement)")
        else:
            print(f"   📊 BASELINE: Achieved {final_rate:.1f} emails/sec (similar to optimized)")
        
        print(f"\n🎯 THEORETICAL MAXIMUM ANALYSIS:")
        network_limit = 1 / 0.4  # Based on 0.4s network latency
        print(f"   🌐 Network-limited max: ~{network_limit:.1f} emails/second")
        efficiency = (final_rate / network_limit) * 100
        print(f"   📊 Achieved efficiency: {efficiency:.1f}% of theoretical maximum")
        
        if efficiency > 60:
            print(f"   🏆 OUTSTANDING: Near-optimal performance achieved!")
        elif efficiency > 40:
            print(f"   ✅ GOOD: Solid performance, room for minor improvements")
        else:
            print(f"   📈 POTENTIAL: Significant room for further optimization")
        
        return self.total_deleted

def main():
    print("🚀 Gmail High Performance Bulk Delete")
    print("⚡ Optimized for maximum speed and efficiency")
    print("📋 Advanced parallel processing for large volumes")
    print("🎯 Starting high performance deletion...")
    print()
    
    try:
        deleter = HighPerformanceDeleter()
        deleter.high_performance_delete()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"\n\n💥 Error: {e}")

if __name__ == "__main__":
    main()