"""Color

This module contains utility constants for styling terminal output.
"""

from enum import Enum


class Color(Enum):
    """ANSI escape sequences for styling terminal text."""

    # colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    # status messages
    INFO = f'{GRAY}[{BLUE}INFO{GRAY}]{RESET}'
    ERROR = f'{GRAY}[{RED}ERROR{GRAY}]{RESET}'
    SUCCESS = f'{GRAY}[{GREEN}SUCCESS{GRAY}]{RESET}'

    # keypress
    ENTER = f'{GRAY}[{YELLOW}ENTER{GRAY}]{RESET}'

    def __str__(self) -> str:
        return self.value
