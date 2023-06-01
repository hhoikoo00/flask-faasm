from .echo import app as echo_app
from .pyperformance import app as pyperformance_app
from .simple import app as simple_app

__all__ = [
    "simple_app",
    "echo_app",
    "pyperformance_app",
]
