# Used to create simple data classes
from dataclasses import dataclass

# Creates a data class for a Bible verse for storing data
@dataclass
class Verse:

    text: str    # Stores the verse text as a string
    reference: str    # Stores the Bible verse reference


