"""Gmail API service implementation following Emex standards."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from googleapiclient.errors import HttpError

from src.types import (
    EmailMessage,
    GmailAPIError,
    GmailSearchQuery,
    MAX_GMAIL_BATCH_SIZE,
    RateLimitError,
)
from src.utils.logger import get_logger
from .auth_service import GmailAuthService

logger = get_logger(__name__)


class GmailService:
    """Gmail API operations following Emex standards."""

    def __init__(self, auth_service: GmailAuthService) -> None:
        """Initialize Gmail service.

        Args:
            auth_service: Authenticated Gmail auth service
        """
        self._auth_service = auth_service
        self._service = None

    def initialize(self) -> None:
        """Initialize the service with authentication."""
        if not self._auth_service.authenticate():
            raise GmailAPIError("Failed to authenticate with Gmail API")
        
        self._service = self._auth_service.get_service()
        logger.info("Gmail service initialized successfully")

    def search_messages(self, search_query: GmailSearchQuery) -> List[str]:
        """Search for message IDs matching criteria.

        Args:
            search_query: Search criteria

        Returns:
            List of Gmail message IDs

        Raises:
            GmailAPIError: If search fails
        """
        if not self._service:
            raise GmailAPIError("Service not initialized")

        query_string = self._build_search_query(search_query)
        logger.info(f"Searching with query: {query_string}")

        try:
            results = self._service.users().messages().list(
                userId="me", q=query_string
            ).execute()

            messages = results.get("messages", [])
            message_ids = [msg["id"] for msg in messages]
            
            logger.info(f"Found {len(message_ids)} messages matching criteria")
            return message_ids

        except HttpError as e:
            if e.resp.status == 429:  # Rate limit
                raise RateLimitError("Rate limit exceeded") from e
            raise GmailAPIError(f"Search failed: {e}") from e

    def get_message_details(self, message_id: str) -> EmailMessage:
        """Get detailed message information.

        Args:
            message_id: Gmail message ID

        Returns:
            Detailed email message data

        Raises:
            GmailAPIError: If retrieval fails
        """
        if not self._service:
            raise GmailAPIError("Service not initialized")

        try:
            message_data = self._service.users().messages().get(
                userId="me", id=message_id, format="metadata",
                metadataHeaders=["From", "To", "Subject", "Date"]
            ).execute()

            return self._parse_message_data(message_data)

        except HttpError as e:
            raise GmailAPIError(f"Failed to get message {message_id}: {e}") from e

    def batch_delete_messages(self, message_ids: List[str]) -> int:
        """Delete messages in batch.

        Args:
            message_ids: List of message IDs to delete

        Returns:
            Number of messages successfully deleted

        Raises:
            GmailAPIError: If deletion fails
        """
        if not self._service:
            raise GmailAPIError("Service not initialized")

        if len(message_ids) > MAX_GMAIL_BATCH_SIZE:
            raise GmailAPIError(
                f"Batch size {len(message_ids)} exceeds limit {MAX_GMAIL_BATCH_SIZE}"
            )

        try:
            self._service.users().messages().batchDelete(
                userId="me", body={"ids": message_ids}
            ).execute()

            logger.info(f"Successfully deleted {len(message_ids)} messages")
            return len(message_ids)

        except HttpError as e:
            if e.resp.status == 429:  # Rate limit
                raise RateLimitError("Rate limit exceeded during deletion") from e
            raise GmailAPIError(f"Batch delete failed: {e}") from e

    def _build_search_query(self, criteria: GmailSearchQuery) -> str:
        """Build Gmail search query string from criteria.

        Args:
            criteria: Search criteria

        Returns:
            Gmail search query string
        """
        query_parts: List[str] = []

        if criteria.older_than_days:
            cutoff_date = self._calculate_cutoff_date(criteria.older_than_days)
            query_parts.append(f"before:{cutoff_date}")

        if criteria.from_addresses:
            from_query = self._build_address_query(criteria.from_addresses, "from")
            query_parts.append(from_query)

        if criteria.subject_contains:
            subject_query = self._build_subject_query(criteria.subject_contains)
            query_parts.append(subject_query)

        if criteria.labels:
            for label in criteria.labels:
                query_parts.append(f"label:{label}")

        if criteria.size_larger_than_mb:
            size_bytes = criteria.size_larger_than_mb * 1024 * 1024
            query_parts.append(f"size:{size_bytes}")

        # Add exclusions
        query_parts.extend(self._build_exclusion_queries(criteria))

        return " ".join(query_parts)

    def _calculate_cutoff_date(self, days_old: int) -> str:
        """Calculate cutoff date for old emails.

        Args:
            days_old: Number of days back

        Returns:
            Date string in YYYY/MM/DD format
        """
        cutoff = datetime.now() - timedelta(days=days_old)
        return cutoff.strftime("%Y/%m/%d")

    def _build_address_query(self, addresses: List[str], field: str) -> str:
        """Build address-based query part.

        Args:
            addresses: List of email addresses
            field: Field name ('from' or 'to')

        Returns:
            Query string for addresses
        """
        address_queries = [f"{field}:{addr}" for addr in addresses]
        return f"({' OR '.join(address_queries)})"

    def _build_subject_query(self, keywords: List[str]) -> str:
        """Build subject-based query part.

        Args:
            keywords: Keywords to search in subject

        Returns:
            Query string for subject keywords
        """
        subject_queries = [f'subject:"{keyword}"' for keyword in keywords]
        return f"({' OR '.join(subject_queries)})"

    def _build_exclusion_queries(self, criteria: GmailSearchQuery) -> List[str]:
        """Build exclusion query parts.

        Args:
            criteria: Search criteria with exclusion flags

        Returns:
            List of exclusion query parts
        """
        exclusions = ["-in:trash", "-in:spam"]  # Always exclude these

        if criteria.exclude_important:
            exclusions.append("-is:important")

        if criteria.exclude_starred:
            exclusions.append("-is:starred")

        if criteria.exclude_with_attachments:
            exclusions.append("-has:attachment")

        return exclusions

    def _parse_message_data(self, message_data: Dict) -> EmailMessage:
        """Parse Gmail API message data into EmailMessage.

        Args:
            message_data: Raw Gmail API message data

        Returns:
            Parsed EmailMessage instance
        """
        headers = self._extract_headers(message_data)
        
        return EmailMessage(
            id=message_data["id"],
            thread_id=message_data["threadId"],
            subject=headers.get("Subject"),
            sender=headers.get("From"),
            recipient=headers.get("To"),
            date=self._parse_date(headers.get("Date")),
            has_attachments=self._has_attachments(message_data),
            is_important=self._is_important(message_data),
            is_starred=self._is_starred(message_data),
            labels=message_data.get("labelIds", []),
            size_bytes=message_data.get("sizeEstimate"),
        )

    def _extract_headers(self, message_data: Dict) -> Dict[str, str]:
        """Extract headers from message data."""
        headers = {}
        for header in message_data.get("payload", {}).get("headers", []):
            headers[header["name"]] = header["value"]
        return headers

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse email date string to datetime."""
        if not date_str:
            return None
        
        try:
            # Basic date parsing - can be enhanced as needed
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None

    def _has_attachments(self, message_data: Dict) -> bool:
        """Check if message has attachments."""
        # Simplified check - can be enhanced for accuracy
        return "attachment" in str(message_data.get("payload", {})).lower()

    def _is_important(self, message_data: Dict) -> bool:
        """Check if message is marked as important."""
        return "IMPORTANT" in message_data.get("labelIds", [])

    def _is_starred(self, message_data: Dict) -> bool:
        """Check if message is starred."""
        return "STARRED" in message_data.get("labelIds", [])