#!/usr/bin/env python3
"""Gmail Bulk Delete - Clean Code Refactored Version"""

import asyncio
from services.deletion_orchestrator import DeletionOrchestrator
from utils.display_helpers import MenuHelper


async def main_async():
    """Main async entry point"""
    print("🚀 Gmail Bulk Delete - Smart Filtering + Async Performance")
    print("⚡ Ultra-fast deletion with intelligent filtering")
    print()
    
    # Get filter configuration from user
    filters = MenuHelper.show_preset_menu()
    
    try:
        orchestrator = DeletionOrchestrator(filters)
        result = await orchestrator.execute_deletion()
        return result
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
        return None
    except Exception as e:
        print(f"\n\n💥 Error: {e}")
        return None


def main():
    """Main entry point"""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()