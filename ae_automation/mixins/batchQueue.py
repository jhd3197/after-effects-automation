"""
Batch Queue Mixin -- Queue and run multiple automation configs sequentially.
"""

from __future__ import annotations

import os
import threading
import time
from typing import Any

from ae_automation.logging_config import get_logger

logger = get_logger(__name__)


class BatchQueueMixin:
    """Queue and run multiple automation configs sequentially."""

    _batch_queue: list[str]
    _batch_status: dict[str, Any]
    _batch_lock: threading.Lock
    _batch_thread: threading.Thread | None

    def _ensure_batch_state(self) -> None:
        """Lazily initialise batch-related attributes if not yet set."""
        if not hasattr(self, "_batch_queue"):
            self._batch_queue = []
        if not hasattr(self, "_batch_status"):
            self._batch_status = {
                "current": 0,
                "total": 0,
                "results": [],
                "running": False,
            }
        if not hasattr(self, "_batch_lock"):
            self._batch_lock = threading.Lock()
        if not hasattr(self, "_batch_thread"):
            self._batch_thread = None

    def queue_config(self, config_path: str) -> int:
        """Add a config to the batch queue. Returns queue position (1-based)."""
        self._ensure_batch_state()
        abs_path = os.path.abspath(config_path)
        if not os.path.isfile(abs_path):
            raise FileNotFoundError(f"Config file not found: {abs_path}")
        with self._batch_lock:
            self._batch_queue.append(abs_path)
            self._batch_status["total"] = len(self._batch_queue)
            return len(self._batch_queue)

    def queue_configs(self, config_paths: list[str]) -> int:
        """Add multiple configs. Returns total queued."""
        self._ensure_batch_state()
        for path in config_paths:
            self.queue_config(path)
        return len(self._batch_queue)

    def start_batch(self) -> None:
        """Start processing the queue sequentially in a background thread."""
        self._ensure_batch_state()
        with self._batch_lock:
            if self._batch_status["running"]:
                logger.warning("Batch is already running")
                return
            if not self._batch_queue:
                logger.warning("Batch queue is empty, nothing to start")
                return
            self._batch_status["running"] = True
            self._batch_status["current"] = 0
            self._batch_status["results"] = []
            self._batch_status["total"] = len(self._batch_queue)

        def _run_batch() -> None:
            queue_snapshot: list[str]
            with self._batch_lock:
                queue_snapshot = list(self._batch_queue)

            for idx, config_path in enumerate(queue_snapshot):
                with self._batch_lock:
                    if not self._batch_status["running"]:
                        # Cancelled
                        break
                    self._batch_status["current"] = idx + 1

                logger.info(
                    "Batch [%d/%d]: processing %s",
                    idx + 1,
                    len(queue_snapshot),
                    config_path,
                )

                result: dict[str, Any] = {
                    "config": config_path,
                    "status": "running",
                    "error": None,
                    "started_at": time.time(),
                    "finished_at": None,
                }

                try:
                    self.startBot(config_path)
                    result["status"] = "success"
                except Exception as exc:
                    result["status"] = "error"
                    result["error"] = str(exc)
                    logger.error("Batch error on %s: %s", config_path, exc)
                finally:
                    result["finished_at"] = time.time()
                    with self._batch_lock:
                        self._batch_status["results"].append(result)

            with self._batch_lock:
                self._batch_status["running"] = False
                self._batch_queue.clear()
            logger.info("Batch processing complete")

        self._batch_thread = threading.Thread(target=_run_batch, daemon=True)
        self._batch_thread.start()

    def get_batch_status(self) -> dict[str, Any]:
        """Return current batch status."""
        self._ensure_batch_state()
        with self._batch_lock:
            return {
                "current": self._batch_status["current"],
                "total": self._batch_status["total"],
                "results": list(self._batch_status["results"]),
                "running": self._batch_status["running"],
            }

    def cancel_batch(self) -> None:
        """Cancel remaining items in the queue."""
        self._ensure_batch_state()
        with self._batch_lock:
            self._batch_status["running"] = False
            self._batch_queue.clear()
        logger.info("Batch cancelled")
