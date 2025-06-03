"""Gmail API type definitions following Emex standards."""

from datetime import datetime
from typing import Dict, List, Optional, Protocol, Union

from pydantic import BaseModel, Field


class EmailMessage(BaseModel):
    """Gmail message data structure."""

    id: str = Field(..., description="Gmail message ID")
    thread_id: str = Field(..., description="Gmail thread ID")
    subject: Optional[str] = Field(None, description="Email subject line")
    sender: Optional[str] = Field(None, description="From email address")
    recipient: Optional[str] = Field(None, description="To email address")
    date: Optional[datetime] = Field(None, description="Email date")
    has_attachments: bool = Field(False, description="Has file attachments")
    is_important: bool = Field(False, description="Marked as important")
    is_starred: bool = Field(False, description="Marked as starred")
    labels: List[str] = Field(default_factory=list, description="Gmail labels")
    size_bytes: Optional[int] = Field(None, description="Email size in bytes")


class EmailHeader(BaseModel):
    """Email header information."""

    name: str = Field(..., description="Header name (e.g., 'From', 'Subject')")
    value: str = Field(..., description="Header value")


class GmailSearchQuery(BaseModel):
    """Gmail search query parameters."""

    older_than_days: Optional[int] = Field(
        None, ge=1, description="Delete emails older than X days"
    )
    from_addresses: Optional[List[str]] = Field(
        None, description="Sender email addresses to target"
    )
    subject_contains: Optional[List[str]] = Field(
        None, description="Keywords that must be in subject"
    )
    labels: Optional[List[str]] = Field(
        None, description="Gmail labels to target"
    )
    size_larger_than_mb: Optional[int] = Field(
        None, ge=1, description="Size threshold in megabytes"
    )
    exclude_important: bool = Field(
        True, description="Skip important emails"
    )
    exclude_starred: bool = Field(True, description="Skip starred emails")
    exclude_with_attachments: bool = Field(
        False, description="Skip emails with attachments"
    )


class BulkDeleteConfig(BaseModel):
    """Configuration for bulk delete operations."""

    search_criteria: GmailSearchQuery = Field(
        ..., description="Email search criteria"
    )
    dry_run: bool = Field(True, description="Test mode without actual deletion")
    batch_size: int = Field(
        100, ge=1, le=1000, description="Emails per batch delete"
    )
    max_concurrent_requests: int = Field(
        5, ge=1, le=10, description="Maximum parallel API requests"
    )
    confirm_deletion: bool = Field(
        True, description="Require user confirmation before deletion"
    )


class DeleteResult(BaseModel):
    """Result of a bulk delete operation."""

    total_found: int = Field(..., description="Total emails found")
    total_deleted: int = Field(..., description="Total emails deleted")
    total_errors: int = Field(..., description="Total errors encountered")
    elapsed_seconds: float = Field(..., description="Operation duration")
    dry_run: bool = Field(..., description="Was this a dry run")
    errors: List[str] = Field(
        default_factory=list, description="Error messages"
    )


class GmailServiceProtocol(Protocol):
    """Protocol defining Gmail service interface."""

    def search_messages(self, query: str) -> List[str]:
        """Search for message IDs matching query."""
        ...

    def get_message_details(self, message_id: str) -> EmailMessage:
        """Get detailed message information."""
        ...

    def batch_delete_messages(self, message_ids: List[str]) -> int:
        """Delete messages in batch, return count of deleted."""
        ...

    def authenticate(self) -> bool:
        """Authenticate with Gmail API."""
        ...


# Constants following Emex rules (no magic numbers)
MAX_GMAIL_BATCH_SIZE = 100
MAX_CONCURRENT_REQUESTS = 5
DEFAULT_RATE_LIMIT_DELAY_MS = 1000
MAX_EMAILS_PER_OPERATION = 10000
GMAIL_API_SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

# Error types
class GmailAPIError(Exception):
    """Gmail API related errors."""

    pass


class AuthenticationError(GmailAPIError):
    """Authentication failures."""

    pass


class RateLimitError(GmailAPIError):
    """Rate limiting errors."""

    pass


class BatchDeleteError(GmailAPIError):
    """Batch deletion failures."""

    pass