"""
Artemis Typing.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ArtemisEntry(object):
    """
    An entry in the export file coming from Artemis.
    """
    matriculation_number: str
    overall_grade: str
    submitted: bool
