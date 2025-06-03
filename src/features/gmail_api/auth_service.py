"""Gmail authentication service following Emex standards."""

import os
import pickle
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.types import (
    GMAIL_API_SCOPES,
    AuthenticationError,
    GmailServiceProtocol,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Constants
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.pickle"


class GmailAuthService:
    """Handles Gmail API authentication following Emex standards."""

    def __init__(
        self,
        credentials_file: str = CREDENTIALS_FILE,
        token_file: str = TOKEN_FILE,
    ) -> None:
        """Initialize authentication service.

        Args:
            credentials_file: Path to OAuth2 credentials JSON
            token_file: Path to store authentication token
        """
        self._credentials_file = credentials_file
        self._token_file = token_file
        self._credentials: Optional[Credentials] = None
        self._service = None

    def authenticate(self) -> bool:
        """Authenticate with Gmail API.

        Returns:
            True if authentication successful

        Raises:
            AuthenticationError: If authentication fails
        """
        try:
            self._credentials = self._load_existing_credentials()
            
            if not self._is_credentials_valid():
                self._refresh_or_create_credentials()
            
            self._save_credentials()
            self._service = self._build_gmail_service()
            
            logger.info("Gmail API authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise AuthenticationError(f"Failed to authenticate: {e}") from e

    def get_service(self):
        """Get authenticated Gmail service.

        Returns:
            Gmail API service instance

        Raises:
            AuthenticationError: If not authenticated
        """
        if not self._service:
            raise AuthenticationError("Not authenticated. Call authenticate() first")
        
        return self._service

    def _load_existing_credentials(self) -> Optional[Credentials]:
        """Load existing credentials from token file."""
        if not os.path.exists(self._token_file):
            return None
            
        try:
            with open(self._token_file, "rb") as token:
                return pickle.load(token)
        except Exception as e:
            logger.warning(f"Failed to load existing token: {e}")
            return None

    def _is_credentials_valid(self) -> bool:
        """Check if current credentials are valid."""
        return (
            self._credentials is not None 
            and self._credentials.valid
        )

    def _refresh_or_create_credentials(self) -> None:
        """Refresh existing credentials or create new ones."""
        if self._can_refresh_credentials():
            self._refresh_credentials()
        else:
            self._create_new_credentials()

    def _can_refresh_credentials(self) -> bool:
        """Check if credentials can be refreshed."""
        return (
            self._credentials is not None
            and self._credentials.expired
            and self._credentials.refresh_token
        )

    def _refresh_credentials(self) -> None:
        """Refresh expired credentials."""
        if not self._credentials:
            raise AuthenticationError("No credentials to refresh")
            
        logger.info("Refreshing expired credentials")
        self._credentials.refresh(Request())

    def _create_new_credentials(self) -> None:
        """Create new credentials through OAuth flow."""
        if not os.path.exists(self._credentials_file):
            raise AuthenticationError(
                f"Credentials file '{self._credentials_file}' not found. "
                "Download from Google Cloud Console."
            )

        logger.info("Starting OAuth flow for new credentials")
        flow = InstalledAppFlow.from_client_secrets_file(
            self._credentials_file, GMAIL_API_SCOPES
        )
        self._credentials = flow.run_local_server(port=0)

    def _save_credentials(self) -> None:
        """Save credentials to token file."""
        if not self._credentials:
            return
            
        try:
            with open(self._token_file, "wb") as token:
                pickle.dump(self._credentials, token)
            logger.debug("Credentials saved successfully")
        except Exception as e:
            logger.warning(f"Failed to save credentials: {e}")

    def _build_gmail_service(self):
        """Build Gmail API service instance."""
        if not self._credentials:
            raise AuthenticationError("No valid credentials available")
            
        return build("gmail", "v1", credentials=self._credentials)