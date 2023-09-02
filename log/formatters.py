from logging import Formatter, LogRecord
from enum import Enum


class ColoredFormatter(Formatter):

    class COLORS(Enum):
        DEBUG = '\033[95m'
        INFO = '\033[96m'
        WARNING = '\033[93m'
        ERROR = '\033[91m'
        CRITICAL = '\033[1m\033[4m'

    ENDC = '\033[0m'

    def format(self, record: LogRecord) -> str:
        message = super().format(record)
        color = getattr(self.COLORS, record.levelname).value
        message = self._paint(message, color)
        return message

    def _paint(self, message: str, color: str) -> str:
        return f"{color}{message}{self.ENDC}"


class EmojiFormatter(Formatter):

    class EMOJIS(Enum):
        DEBUG = '🪲'
        INFO = '👀'
        WARNING = '⚠️'
        ERROR = '🚨'
        CRITICAL = '☠️‼️‼️‼️☠️'

    def format(self, record: LogRecord) -> str:
        message = super().format(record)
        emoji = getattr(self.EMOJIS, record.levelname).value
        message = self._paint(message, emoji)
        return message

    def _paint(self, message: str, emoji: str):
        return f'{emoji} {message}'
