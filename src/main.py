"""Main entry point for Gmail bulk delete application."""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from src.config import ConfigManager
from src.features.bulk_operations import BulkDeleteService
from src.features.gmail_api import GmailAuthService, GmailService
from src.types import GmailAPIError
from src.utils import get_logger, setup_file_logging

console = Console()
logger = get_logger(__name__)


@click.group()
@click.option("--config", default="config.json", help="Configuration file path")
@click.option("--log-level", default="INFO", help="Logging level")
@click.option("--log-file", help="Log file path")
@click.pass_context
def cli(ctx, config: str, log_level: str, log_file: str) -> None:
    """Gmail Bulk Delete Tool - Secure email management following Emex standards."""
    ctx.ensure_object(dict)
    
    # Setup logging
    global logger
    logger = get_logger(__name__, log_level)
    
    if log_file:
        setup_file_logging(logger, log_file)
    
    # Initialize configuration manager
    ctx.obj["config_manager"] = ConfigManager(config)
    ctx.obj["config_file"] = config


@cli.command()
@click.option("--rule", help="Use predefined rule")
@click.option("--dry-run/--no-dry-run", default=True, help="Dry run mode")
@click.pass_context
def delete(ctx, rule: str, dry_run: bool) -> None:
    """Execute bulk delete operation."""
    config_manager = ctx.obj["config_manager"]
    
    try:
        # Load configuration
        if rule:
            config = config_manager.create_config_from_rules(rule)
            console.print(f"📋 Using rule: [bold]{rule}[/bold]")
        else:
            config = config_manager.load_config()
            console.print("📋 Using configuration from file")
        
        # Override dry-run if specified
        if not dry_run:
            config.dry_run = False
        
        # Display configuration
        _display_config(config)
        
        # Initialize services
        auth_service = GmailAuthService()
        gmail_service = GmailService(auth_service)
        gmail_service.initialize()
        
        bulk_service = BulkDeleteService(gmail_service)
        
        # Execute operation
        result = bulk_service.execute_bulk_delete(config)
        
        # Display results
        _display_results(result)
        
    except Exception as e:
        console.print(f"❌ [red]Error: {e}[/red]")
        logger.error(f"Delete operation failed: {e}")
        sys.exit(1)


@cli.command()
@click.option("--rule", help="Use predefined rule")
@click.pass_context
def preview(ctx, rule: str) -> None:
    """Preview emails that would be deleted."""
    config_manager = ctx.obj["config_manager"]
    
    try:
        # Load configuration
        if rule:
            config = config_manager.create_config_from_rules(rule)
            console.print(f"📋 Using rule: [bold]{rule}[/bold]")
        else:
            config = config_manager.load_config()
        
        # Force dry run for preview
        config.dry_run = True
        
        # Initialize services
        auth_service = GmailAuthService()
        gmail_service = GmailService(auth_service)
        gmail_service.initialize()
        
        bulk_service = BulkDeleteService(gmail_service)
        
        # Get preview
        preview_emails = bulk_service.preview_deletion(config)
        
        if not preview_emails:
            console.print("✅ No emails found matching criteria")
            return
        
        # Display preview
        _display_preview(preview_emails)
        
    except Exception as e:
        console.print(f"❌ [red]Error: {e}[/red]")
        logger.error(f"Preview operation failed: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def rules(ctx) -> None:
    """List available deletion rules."""
    config_manager = ctx.obj["config_manager"]
    
    try:
        available_rules = config_manager.list_available_rules()
        rules_data = config_manager.load_rules()
        
        if not available_rules:
            console.print("No rules available")
            return
        
        # Create table
        table = Table(title="Available Deletion Rules")
        table.add_column("Rule Name", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Criteria", style="yellow")
        
        for rule_name in available_rules:
            rule_info = rules_data[rule_name]
            criteria_summary = _summarize_criteria(rule_info.get("criteria", {}))
            
            table.add_row(
                rule_name,
                rule_info.get("description", "No description"),
                criteria_summary
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ [red]Error loading rules: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--rule", help="Create config from rule")
@click.pass_context
def config(ctx, rule: str) -> None:
    """Generate configuration file."""
    config_manager = ctx.obj["config_manager"]
    config_file = ctx.obj["config_file"]
    
    try:
        if rule:
            config = config_manager.create_config_from_rules(rule)
            console.print(f"📋 Creating config from rule: [bold]{rule}[/bold]")
        else:
            config = config_manager._create_default_config()
            console.print("📋 Creating default configuration")
        
        config_manager.save_config(config)
        console.print(f"✅ Configuration saved to: [bold]{config_file}[/bold]")
        
    except Exception as e:
        console.print(f"❌ [red]Error creating config: {e}[/red]")
        sys.exit(1)


def _display_config(config) -> None:
    """Display current configuration."""
    console.print("\n📊 [bold]Configuration:[/bold]")
    console.print(f"  Dry Run: [cyan]{config.dry_run}[/cyan]")
    console.print(f"  Batch Size: [cyan]{config.batch_size}[/cyan]")
    
    criteria = config.search_criteria
    console.print("\n🔍 [bold]Search Criteria:[/bold]")
    
    if criteria.older_than_days:
        console.print(f"  Older than: [yellow]{criteria.older_than_days} days[/yellow]")
    
    if criteria.exclude_with_attachments:
        console.print("  Exclude: [green]Emails with attachments[/green]")
    
    if criteria.exclude_important:
        console.print("  Exclude: [green]Important emails[/green]")
    
    if criteria.exclude_starred:
        console.print("  Exclude: [green]Starred emails[/green]")


def _display_results(result) -> None:
    """Display operation results."""
    console.print("\n📈 [bold]Results:[/bold]")
    
    if result.dry_run:
        console.print(f"  🧪 [yellow]DRY RUN - No emails were actually deleted[/yellow]")
    
    console.print(f"  📧 Found: [cyan]{result.total_found}[/cyan] emails")
    console.print(f"  🗑️  Deleted: [green]{result.total_deleted}[/green] emails")
    
    if result.total_errors > 0:
        console.print(f"  ❌ Errors: [red]{result.total_errors}[/red]")
    
    console.print(f"  ⏱️  Time: [cyan]{result.elapsed_seconds:.2f}s[/cyan]")
    
    if result.total_deleted > 0:
        rate = result.total_deleted / result.elapsed_seconds
        console.print(f"  📊 Rate: [cyan]{rate:.1f} emails/sec[/cyan]")


def _display_preview(emails) -> None:
    """Display email preview."""
    console.print(f"\n📋 [bold]Preview ({len(emails)} emails):[/bold]")
    
    for i, email in enumerate(emails, 1):
        console.print(f"\n{i}. [bold]{email.subject or 'No Subject'}[/bold]")
        console.print(f"   From: [cyan]{email.sender or 'Unknown'}[/cyan]")
        console.print(f"   Date: [yellow]{email.date or 'Unknown'}[/yellow]")
        
        if email.has_attachments:
            console.print("   📎 [green]Has attachments[/green]")


def _summarize_criteria(criteria: dict) -> str:
    """Summarize search criteria for display."""
    parts = []
    
    if criteria.get("older_than_days"):
        parts.append(f">{criteria['older_than_days']}d")
    
    if criteria.get("exclude_with_attachments"):
        parts.append("no attachments")
    
    if criteria.get("subject_contains"):
        parts.append(f"subjects: {', '.join(criteria['subject_contains'][:2])}")
    
    if criteria.get("labels"):
        parts.append(f"labels: {', '.join(criteria['labels'][:2])}")
    
    return ", ".join(parts) if parts else "No specific criteria"


def main() -> None:
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()