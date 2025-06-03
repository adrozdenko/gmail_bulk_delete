"""Application settings and configuration management."""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseSettings, Field, validator

from src.types import BulkDeleteConfig, GmailSearchQuery


class AppSettings(BaseSettings):
    """Application settings with environment variable support."""

    # Gmail API Configuration
    credentials_file: str = Field(
        default="credentials.json",
        description="Path to Gmail API credentials file"
    )
    token_file: str = Field(
        default="token.pickle",
        description="Path to store authentication token"
    )

    # Application Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(
        default=None, description="Optional log file path"
    )
    config_file: str = Field(
        default="config.json", description="Configuration file path"
    )

    # Operation Defaults
    default_batch_size: int = Field(
        default=100, ge=1, le=1000, description="Default batch size"
    )
    default_dry_run: bool = Field(
        default=True, description="Default dry run mode"
    )
    confirm_deletion: bool = Field(
        default=True, description="Require deletion confirmation"
    )

    class Config:
        """Pydantic configuration."""

        env_prefix = "GMAIL_DELETE_"
        case_sensitive = False
        env_file = ".env"


class ConfigManager:
    """Manages application configuration and rule sets."""

    def __init__(self, config_file: str = "config.json") -> None:
        """Initialize configuration manager.

        Args:
            config_file: Path to configuration file
        """
        self._config_file = Path(config_file)
        self._rules: Dict = {}
        self._settings = AppSettings()

    def load_config(self) -> BulkDeleteConfig:
        """Load configuration from file.

        Returns:
            Bulk delete configuration
        """
        if not self._config_file.exists():
            return self._create_default_config()

        try:
            with open(self._config_file, "r") as f:
                config_data = json.load(f)

            return self._parse_config_data(config_data)

        except Exception as e:
            raise ValueError(f"Failed to load config from {self._config_file}: {e}")

    def save_config(self, config: BulkDeleteConfig) -> None:
        """Save configuration to file.

        Args:
            config: Configuration to save
        """
        config_data = {
            "search_criteria": config.search_criteria.dict(),
            "dry_run": config.dry_run,
            "batch_size": config.batch_size,
            "max_concurrent_requests": config.max_concurrent_requests,
            "confirm_deletion": config.confirm_deletion,
        }

        with open(self._config_file, "w") as f:
            json.dump(config_data, f, indent=2)

    def load_rules(self, rules_file: str = "rules.json") -> Dict:
        """Load email filtering rules from file.

        Args:
            rules_file: Path to rules file

        Returns:
            Dictionary of rules
        """
        rules_path = Path(rules_file)

        if not rules_path.exists():
            return self._create_default_rules()

        try:
            with open(rules_path, "r") as f:
                return json.load(f)

        except Exception as e:
            raise ValueError(f"Failed to load rules from {rules_path}: {e}")

    def create_config_from_rules(self, rule_name: str) -> BulkDeleteConfig:
        """Create configuration from predefined rule.

        Args:
            rule_name: Name of the rule to use

        Returns:
            Configuration based on rule

        Raises:
            ValueError: If rule not found
        """
        if not self._rules:
            self._rules = self.load_rules()

        if rule_name not in self._rules:
            available_rules = list(self._rules.keys())
            raise ValueError(
                f"Rule '{rule_name}' not found. Available: {available_rules}"
            )

        rule_data = self._rules[rule_name]
        search_criteria = GmailSearchQuery(**rule_data.get("criteria", {}))

        return BulkDeleteConfig(
            search_criteria=search_criteria,
            dry_run=rule_data.get("dry_run", self._settings.default_dry_run),
            batch_size=rule_data.get("batch_size", self._settings.default_batch_size),
            confirm_deletion=rule_data.get("confirm_deletion", self._settings.confirm_deletion),
        )

    def list_available_rules(self) -> List[str]:
        """Get list of available rule names.

        Returns:
            List of rule names
        """
        if not self._rules:
            self._rules = self.load_rules()

        return list(self._rules.keys())

    def get_settings(self) -> AppSettings:
        """Get application settings.

        Returns:
            Application settings
        """
        return self._settings

    def _create_default_config(self) -> BulkDeleteConfig:
        """Create default configuration.

        Returns:
            Default bulk delete configuration
        """
        search_criteria = GmailSearchQuery(
            older_than_days=180,  # 6 months
            exclude_important=True,
            exclude_starred=True,
            exclude_with_attachments=True,
        )

        return BulkDeleteConfig(
            search_criteria=search_criteria,
            dry_run=self._settings.default_dry_run,
            batch_size=self._settings.default_batch_size,
            confirm_deletion=self._settings.confirm_deletion,
        )

    def _parse_config_data(self, config_data: Dict) -> BulkDeleteConfig:
        """Parse configuration data into BulkDeleteConfig.

        Args:
            config_data: Raw configuration data

        Returns:
            Parsed configuration
        """
        search_criteria = GmailSearchQuery(**config_data.get("search_criteria", {}))

        return BulkDeleteConfig(
            search_criteria=search_criteria,
            dry_run=config_data.get("dry_run", self._settings.default_dry_run),
            batch_size=config_data.get("batch_size", self._settings.default_batch_size),
            max_concurrent_requests=config_data.get(
                "max_concurrent_requests", 5
            ),
            confirm_deletion=config_data.get(
                "confirm_deletion", self._settings.confirm_deletion
            ),
        )

    def _create_default_rules(self) -> Dict:
        """Create default rule set.

        Returns:
            Default rules dictionary
        """
        return {
            "keep_attachments_6months": {
                "description": "Delete emails older than 6 months, keep attachments",
                "criteria": {
                    "older_than_days": 180,
                    "exclude_important": True,
                    "exclude_starred": True,
                    "exclude_with_attachments": True,
                },
                "dry_run": True,
            },
            "newsletter_cleanup": {
                "description": "Clean up newsletters and promotions",
                "criteria": {
                    "older_than_days": 30,
                    "subject_contains": ["Newsletter", "Unsubscribe", "Promotion"],
                    "labels": ["promotions"],
                    "exclude_important": True,
                    "exclude_starred": True,
                },
                "dry_run": True,
            },
            "large_emails_cleanup": {
                "description": "Remove large emails older than 3 months",
                "criteria": {
                    "older_than_days": 90,
                    "size_larger_than_mb": 10,
                    "exclude_important": True,
                    "exclude_starred": True,
                },
                "dry_run": True,
            },
            "social_cleanup": {
                "description": "Clean up social media notifications",
                "criteria": {
                    "older_than_days": 60,
                    "labels": ["social"],
                    "exclude_important": True,
                    "exclude_starred": True,
                },
                "dry_run": True,
            },
        }