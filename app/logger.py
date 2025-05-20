# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/logger.py
# This module defines a unified logger using rich for colorful terminal output.

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from rich.console import Console
from rich.traceback import install

# Enable rich traceback with local variable display
install(show_locals=True)


class RichLogger:
    def __init__(self):
        self.console = Console()

    def info(self, message: str):
        self.console.print(f"[cyan][INFO] {message}[/]")

    def success(self, message: str):
        self.console.print(f"[green][SUCCESS] {message}[/]")

    def error(self, message: str):
        self.console.print(f"[bold red][ERROR] {message}[/]")

    def warning(self, message: str):
        self.console.print(f"[yellow][WARNING] {message}[/]")

    def rule(self, message: str):
        self.console.rule(message)

    def print(self, *args, **kwargs):
        self.console.print(*args, **kwargs)


# global unified logger
logger = RichLogger()

if __name__ == "__main__":
    # Example usage
    logger.info("This is an info message.")
    logger.success("This is a success message.")
    logger.error("This is an error message.")
    logger.warning("This is a warning message.")
    logger.rule("This is a rule message.")
    logger.print("This is a custom print message.")