"""Crimson Desert Trainer - community memory-editing toolkit."""

__version__ = "1.4.2"
__game__ = "Crimson Desert"
__supported_builds__ = ("1.0.7", "1.0.8", "1.0.9")

from .bootstrap import TrainerApp

__all__ = ["TrainerApp", "__version__", "__supported_builds__"]