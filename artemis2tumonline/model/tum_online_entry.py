"""
TUM Online Typing.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class TumOnlineEntry(object):
    """
    An Entry of the TUMOnline CSV.
    """
    registration_number: str
    number_of_the_course: str
    date_of_assessment: str
    remark: str
    ects_grade: str
    db_primary_key_of_candidate: str
    db_primary_key_of_exam: str


@dataclass(frozen=True)
class TumOnlineEntryWithGrade(TumOnlineEntry):
    """
    An Entry of the TUMOnline CSV with the grade.
    """
    grade: str
