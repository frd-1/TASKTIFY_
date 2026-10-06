from dataclasses import dataclass


@dataclass
class Verse:
    """Data model representing a Bible verse."""

    text: str
    reference: str