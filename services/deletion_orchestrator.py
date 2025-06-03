#!/usr/bin/env python3
"""Main deletion orchestration service"""

import asyncio
import time
from typing import Dict, List
from datetime import datetime

from services.gmail_client import GmailClient
from services.query_builder import QueryBuilder
from services.email_deleter import EmailDeleter
from services.performance_tracker import PerformanceTracker
from utils.display_helpers import FilterDisplayHelper, ProgressDisplayHelper
from constants import (
    EMAILS_PER_CHUNK, MAX_CONCURRENT_TASKS, EMAILS_PER_TASK,
    STANDARD_DELAY, ERROR_RECOVERY_DELAY
)


class DeletionOrchestrator:
    """Orchestrates the email deletion process"""
    
    def __init__(self, filters: Dict):
        self.filters = filters
        self.gmail_client = GmailClient()
        self.query_builder = QueryBuilder(filters)
        self.email_deleter = EmailDeleter(self.gmail_client)
        self.performance_tracker = PerformanceTracker()
        self.display_helper = FilterDisplayHelper()
    
    async def execute_deletion(self) -> dict:
        """Execute the complete deletion process"""
        self._print_header()
        
        query = self.query_builder.build_query()
        self._print_query_info(query)
        
        initial_count = await self._get_initial_count(query)
        self._print_performance_settings()
        
        self.performance_tracker.start_tracking()
        
        result = await self._run_deletion_loop(query, initial_count)
        
        return self._finalize_deletion()
    
    def _print_header(self):
        """Print deletion process header"""
        print("🚀 ASYNC HIGH PERFORMANCE GMAIL DELETION")
        print("⚡ Optimized with async/await for maximum speed")
        print("💾 Memory-optimized for minimal RAM usage")
        print("=" * 60)
    
    def _print_query_info(self, query: str):
        """Print query and filter information"""
        print(f"📧 Gmail Query: {query}")
        print()
        self.display_helper.print_filter_summary(self.filters)
    
    async def _get_initial_count(self, query: str) -> int:
        """Get initial email count estimate"""
        print("📊 Analyzing emails...")
        count = await self.gmail_client.get_initial_email_count(query)
        print(f"📧 Initial estimate: {count} emails")
        return count
    
    def _print_performance_settings(self):
        """Print performance configuration"""
        print("\n⚡ MAXIMUM PERFORMANCE MODE:")
        print("   🚀 Batch API optimization enabled")
        print("   ⚡ Async/await concurrent processing")
        print(f"   🧵 {MAX_CONCURRENT_TASKS} concurrent async tasks")
        print(f"   📦 {EMAILS_PER_CHUNK} emails per chunk, {EMAILS_PER_TASK} per task")
        print("   💾 Memory optimized")
        print()
        print(f"⚙️  Settings: {EMAILS_PER_CHUNK} emails/chunk, {MAX_CONCURRENT_TASKS} async tasks, {EMAILS_PER_TASK} emails/task")
        print("=" * 60)
    
    async def _run_deletion_loop(self, query: str, initial_count: int) -> bool:
        """Run the main deletion loop"""
        batch_number = 1
        
        while True:
            message_ids = await self._get_email_batch(query)
            if not message_ids:
                break
            
            success = await self._process_single_batch(
                message_ids, batch_number, initial_count
            )
            
            if not success:
                await asyncio.sleep(ERROR_RECOVERY_DELAY)
            
            batch_number += 1
            await self._post_batch_maintenance(batch_number)
        
        return True
    
    async def _get_email_batch(self, query: str) -> List[str]:
        """Get next batch of emails to process"""
        return await self.gmail_client.get_email_batch(query, EMAILS_PER_CHUNK)
    
    async def _process_single_batch(self, message_ids: List[str], 
                                   batch_number: int, initial_count: int) -> bool:
        """Process a single batch of emails"""
        try:
            batch_start_time = time.time()
            
            print(f"\n📦 BATCH {batch_number}")
            print(f"   📧 Processing {len(message_ids)} emails with {MAX_CONCURRENT_TASKS} async tasks...")
            
            await self._execute_batch_deletion(message_ids)
            
            self._print_batch_results(batch_number, len(message_ids), 
                                    batch_start_time, initial_count)
            return True
            
        except Exception as e:
            print(f"\n💥 Error in batch {batch_number}: {e}")
            return False
    
    async def _execute_batch_deletion(self, message_ids: List[str]):
        """Execute deletion for a batch using async tasks"""
        task_batches = self._create_task_batches(message_ids)
        
        # Create and run async tasks with semaphore for concurrency control
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
        tasks = []
        
        for i, batch in enumerate(task_batches):
            task = self._create_bounded_deletion_task(batch, i, semaphore)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        self._process_task_results(results)
    
    def _create_task_batches(self, message_ids: List[str]) -> List[List[str]]:
        """Split message IDs into task batches"""
        return [
            message_ids[i:i + EMAILS_PER_TASK] 
            for i in range(0, len(message_ids), EMAILS_PER_TASK)
        ]
    
    async def _create_bounded_deletion_task(self, batch: List[str], 
                                          task_id: int, semaphore):
        """Create bounded async deletion task"""
        async with semaphore:
            return await self.email_deleter.delete_email_batch(batch)
    
    def _process_task_results(self, results: List):
        """Process results from async tasks"""
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"   💥 Task {i} crashed: {result}")
            else:
                deleted, errors = result
                self.performance_tracker.update_stats(deleted, errors)
                if errors > 0:
                    print(f"   🔧 Task {i}: {deleted} ✅, {errors} ❌")
                else:
                    print(f"   🔧 Task {i}: {deleted} ✅")
    
    def _print_batch_results(self, batch_number: int, email_count: int, 
                           start_time: float, initial_count: int):
        """Print results for completed batch"""
        duration = time.time() - start_time
        current_rate = email_count / duration if duration > 0 else 0
        overall_rate = self.performance_tracker.get_current_rate(
            self.performance_tracker.stats.total_deleted
        )
        
        self.performance_tracker.record_batch_performance(email_count, duration)
        
        ProgressDisplayHelper.print_batch_stats(
            batch_number, email_count, duration, current_rate,
            self.performance_tracker.stats.total_deleted,
            self.performance_tracker.get_memory_usage_mb()
        )
        
        print(f"   📊 Overall rate: {overall_rate:.1f} emails/second")
        
        recent_avg = self.performance_tracker.get_recent_average_rate()
        print(f"   📈 Recent avg: {recent_avg:.1f} emails/second")
        
        if self.email_deleter.rate_limit_counter > 0:
            print(f"   ⚠️  Rate limits hit: {self.email_deleter.rate_limit_counter} times")
        
        ProgressDisplayHelper.print_progress_bar(
            self.performance_tracker.stats.total_deleted, initial_count
        )
        
        if self.performance_tracker.should_print_periodic_status():
            print(f"   📈 Performance: {overall_rate:.1f} emails/sec average")
    
    async def _post_batch_maintenance(self, batch_number: int):
        """Perform post-batch maintenance"""
        self.performance_tracker.perform_maintenance_if_needed(batch_number)
        await self._apply_rate_limiting()
    
    async def _apply_rate_limiting(self):
        """Apply rate limiting based on current conditions"""
        if self.email_deleter.rate_limit_counter > 0:
            delay = min(0.1 * (self.email_deleter.rate_limit_counter / 10), 1.0)
            await asyncio.sleep(delay)
        else:
            await asyncio.sleep(STANDARD_DELAY)
    
    def _finalize_deletion(self) -> dict:
        """Finalize deletion and return results"""
        results = self.performance_tracker.get_final_results()
        self._print_final_results(results)
        return results
    
    def _print_final_results(self, results: dict):
        """Print final deletion results"""
        print("\n" + "=" * 60)
        print("🎉 HIGH PERFORMANCE DELETION COMPLETE!")
        print("=" * 60)
        print(f"📊 RESULTS:")
        print(f"   🗑️  Total deleted: {results['total_deleted']}")
        print(f"   ❌ Total errors: {results['total_errors']}")
        print(f"   ⏱️  Duration: {results['duration_seconds']:.1f} seconds")
        print(f"   🚀 Average rate: {results['deletion_rate']:.1f} emails/second")
        print(f"   ✅ Success rate: {results['success_rate']:.1f}%")
        print(f"   🚀 Batch API efficiency: {results['batch_api_efficiency']:.1f}%")
        print(f"   🔗 Connection reuses: {results['connection_reuses']}")
        if results['connection_reuses'] > 1:
            print(f"   🔗 Connection pooling: ✅ Active ({results['connection_reuses']} reuses)")