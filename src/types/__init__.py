"""Type definitions for Gmail bulk delete application."""

from .gmail import (
    AuthenticationError,
    BatchDeleteError,
    BulkDeleteConfig,
    DeleteResult,
    EmailMessage,
    GmailAPIError,
    GmailSearchQuery,
    GmailServiceProtocol,
    RateLimitError,
    MAX_GMAIL_BATCH_SIZE,
    MAX_CONCURRENT_REQUESTS,
    DEFAULT_RATE_LIMIT_DELAY_MS,
    MAX_EMAILS_PER_OPERATION,
    GMAIL_API_SCOPES,
)

__all__ = [
    "AuthenticationError",
    "BatchDeleteError",
    "BulkDeleteConfig",
    "DeleteResult",
    "EmailMessage",
    "GmailAPIError",
    "GmailSearchQuery",
    "GmailServiceProtocol",
    "RateLimitError",
    "MAX_GMAIL_BATCH_SIZE",
    "MAX_CONCURRENT_REQUESTS",
    "DEFAULT_RATE_LIMIT_DELAY_MS",
    "MAX_EMAILS_PER_OPERATION",
    "GMAIL_API_SCOPES",
]