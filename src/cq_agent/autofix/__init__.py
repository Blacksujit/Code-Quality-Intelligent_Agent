# Autofix module for automated code fixes
from .auto import compute_autofixes, generate_patch, apply_edits

__all__ = ["compute_autofixes", "generate_patch", "apply_edits"]
