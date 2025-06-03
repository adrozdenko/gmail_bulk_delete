"""Bulk delete service following Emex standards."""

import time
from typing import List

from src.features.gmail_api import GmailService
from src.types import (
    BulkDeleteConfig,
    DeleteResult,
    EmailMessage,
    GmailAPIError,
    MAX_GMAIL_BATCH_SIZE,
)
from src.utils.logger import get_logger
from .progress_tracker import ProgressTracker

logger = get_logger(__name__)


class BulkDeleteService:
    """Service for bulk email deletion operations."""

    def __init__(self, gmail_service: GmailService) -> None:
        """Initialize bulk delete service.

        Args:
            gmail_service: Gmail API service instance
        """
        self._gmail_service = gmail_service
        self._progress_tracker = ProgressTracker()

    def execute_bulk_delete(self, config: BulkDeleteConfig) -> DeleteResult:
        """Execute bulk delete operation.

        Args:
            config: Bulk delete configuration

        Returns:
            Results of the delete operation

        Raises:
            GmailAPIError: If operation fails
        """
        start_time = time.time()
        
        logger.info(f"Starting bulk delete operation (dry_run={config.dry_run})")
        
        try:
            # Search for messages
            message_ids = self._search_messages(config)
            
            if not message_ids:
                return self._create_empty_result(config.dry_run, start_time)
            
            # Show preview if not dry run
            if not config.dry_run and config.confirm_deletion:
                if not self._confirm_deletion(message_ids):
                    logger.info("Deletion cancelled by user")
                    return self._create_empty_result(config.dry_run, start_time)
            
            # Execute deletion
            deleted_count = self._delete_messages(message_ids, config)
            
            elapsed = time.time() - start_time
            
            return DeleteResult(
                total_found=len(message_ids),
                total_deleted=deleted_count,
                total_errors=len(message_ids) - deleted_count,
                elapsed_seconds=elapsed,
                dry_run=config.dry_run,
                errors=[]
            )
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"Bulk delete operation failed: {e}")
            
            return DeleteResult(
                total_found=0,
                total_deleted=0,
                total_errors=1,
                elapsed_seconds=elapsed,
                dry_run=config.dry_run,
                errors=[str(e)]
            )

    def preview_deletion(self, config: BulkDeleteConfig) -> List[EmailMessage]:
        """Preview emails that would be deleted.

        Args:
            config: Bulk delete configuration

        Returns:
            List of email messages that would be deleted (max 10)
        """
        message_ids = self._search_messages(config)
        
        if not message_ids:
            return []
        
        # Get details for first few messages as preview
        preview_ids = message_ids[:10]  # Preview limit
        preview_messages = []
        
        for message_id in preview_ids:
            try:
                message = self._gmail_service.get_message_details(message_id)
                preview_messages.append(message)
            except GmailAPIError as e:
                logger.warning(f"Failed to get preview for {message_id}: {e}")
        
        return preview_messages

    def _search_messages(self, config: BulkDeleteConfig) -> List[str]:
        """Search for messages matching criteria.

        Args:
            config: Bulk delete configuration

        Returns:
            List of message IDs
        """
        logger.info("Searching for messages matching criteria")
        return self._gmail_service.search_messages(config.search_criteria)

    def _delete_messages(
        self, 
        message_ids: List[str], 
        config: BulkDeleteConfig
    ) -> int:
        """Delete messages in batches.

        Args:
            message_ids: List of message IDs to delete
            config: Configuration with batch settings

        Returns:
            Number of successfully deleted messages
        """
        if config.dry_run:
            logger.info(f"DRY RUN: Would delete {len(message_ids)} messages")
            return 0

        total_deleted = 0
        batch_size = min(config.batch_size, MAX_GMAIL_BATCH_SIZE)
        
        self._progress_tracker.start(len(message_ids))
        
        for i in range(0, len(message_ids), batch_size):
            batch = message_ids[i:i + batch_size]
            
            try:
                deleted_count = self._gmail_service.batch_delete_messages(batch)
                total_deleted += deleted_count
                
                self._progress_tracker.update(deleted_count)
                logger.info(f"Deleted batch: {deleted_count} messages")
                
                # Rate limiting delay
                if i + batch_size < len(message_ids):
                    time.sleep(0.1)  # Small delay between batches
                    
            except GmailAPIError as e:
                logger.error(f"Failed to delete batch starting at {i}: {e}")
                continue
        
        self._progress_tracker.complete()
        return total_deleted

    def _confirm_deletion(self, message_ids: List[str]) -> bool:
        """Ask user to confirm deletion.

        Args:
            message_ids: List of message IDs to delete

        Returns:
            True if user confirms deletion
        """
        total_count = len(message_ids)
        
        print(f"\n⚠️  About to delete {total_count} emails")
        print("This action cannot be undone!")
        
        response = input("Type 'yes' to confirm deletion: ").strip().lower()
        return response == "yes"

    def _create_empty_result(
        self, 
        dry_run: bool, 
        start_time: float
    ) -> DeleteResult:
        """Create empty result for no-op operations.

        Args:
            dry_run: Whether this was a dry run
            start_time: Operation start time

        Returns:
            Empty delete result
        """
        elapsed = time.time() - start_time
        
        return DeleteResult(
            total_found=0,
            total_deleted=0,
            total_errors=0,
            elapsed_seconds=elapsed,
            dry_run=dry_run,
            errors=[]
        )