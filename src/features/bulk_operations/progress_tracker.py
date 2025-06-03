"""Progress tracking for bulk operations."""

import time
from typing import Optional

from rich.console import Console
from rich.progress import Progress, TaskID

from src.utils.logger import get_logger

logger = get_logger(__name__)


class ProgressTracker:
    """Tracks and displays progress for bulk operations."""

    def __init__(self) -> None:
        """Initialize progress tracker."""
        self._console = Console()
        self._progress: Optional[Progress] = None
        self._task_id: Optional[TaskID] = None
        self._start_time: Optional[float] = None
        self._total_items = 0
        self._completed_items = 0

    def start(self, total_items: int) -> None:
        """Start progress tracking.

        Args:
            total_items: Total number of items to process
        """
        self._total_items = total_items
        self._completed_items = 0
        self._start_time = time.time()

        self._progress = Progress()
        self._progress.start()

        self._task_id = self._progress.add_task(
            "Deleting emails...", total=total_items
        )

        logger.info(f"Started progress tracking for {total_items} items")

    def update(self, items_completed: int) -> None:
        """Update progress.

        Args:
            items_completed: Number of additional items completed
        """
        if not self._progress or self._task_id is None:
            return

        self._completed_items += items_completed
        self._progress.update(self._task_id, completed=self._completed_items)

        # Log milestone progress
        if self._completed_items % 100 == 0 or self._completed_items == self._total_items:
            percentage = (self._completed_items / self._total_items) * 100
            logger.info(f"Progress: {self._completed_items}/{self._total_items} ({percentage:.1f}%)")

    def complete(self) -> None:
        """Complete progress tracking."""
        if not self._progress:
            return

        self._progress.stop()

        if self._start_time:
            elapsed = time.time() - self._start_time
            rate = self._completed_items / elapsed if elapsed > 0 else 0

            self._console.print(
                f"✅ Completed! {self._completed_items} items in {elapsed:.2f}s "
                f"({rate:.1f} items/sec)"
            )

        logger.info(f"Progress tracking completed: {self._completed_items} items")

    def get_stats(self) -> dict:
        """Get current progress statistics.

        Returns:
            Dictionary with progress stats
        """
        elapsed = time.time() - self._start_time if self._start_time else 0
        rate = self._completed_items / elapsed if elapsed > 0 else 0

        return {
            "total_items": self._total_items,
            "completed_items": self._completed_items,
            "elapsed_seconds": elapsed,
            "rate_per_second": rate,
            "percentage": (self._completed_items / self._total_items) * 100 if self._total_items > 0 else 0
        }