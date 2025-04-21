"""
Entities package for the KorwinAI Discord Bot.

This package contains the core domain entities used by the application.
"""

from entities.catalogue import LocalCache, Category, KorwinCatalogue

__all__ = ["KorwinCatalogue", "Category", "LocalCache"]
