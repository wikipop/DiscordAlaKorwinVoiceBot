"""
Category module for the KorwinAI Discord Bot.

This module defines the Category enum used to categorize text and audio segments
in the Korwin catalogue.
"""

import enum


class Category(enum.Enum):
    """
    Enum representing different categories of text and audio segments in the Korwin catalogue.
    
    Each category corresponds to a specific part of a generated sentence.
    """
    INTRO = "Intro"
    PODMIOT = "Podmiot"
    CECHY = "Cechy"
    DZIALANIE = "Działanie"
    UZASADNIENIE = "Uzasadnienie"
    KOMENTARZ = "Komentarz"