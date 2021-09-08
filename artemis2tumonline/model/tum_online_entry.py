"""
TUM Online Typing.
"""
from collections import Sequence
from dataclasses import asdict, dataclass

from artemis2tumonline.model.artemis_entry import ArtemisEntry


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

    def create_entry_with_grade(self, artemis_entries: Sequence[ArtemisEntry]) -> "TumOnlineEntryWithGrade":
        """
        Finds the matching Artemis entry and derives the grade from it.
        :param artemis_entries:
        :return:
        """
        artemis_entry = next(a for a in artemis_entries if a.matriculation_number == self.registration_number)
        grade: str = artemis_entry.overall_grade if artemis_entry.submitted else "X-5.0"
        return TumOnlineEntryWithGrade(
                grade=grade,
                **asdict(self)
        )


@dataclass(frozen=True)
class TumOnlineEntryWithGrade(TumOnlineEntry):
    """
    An Entry of the TUMOnline CSV with the grade.
    """
    grade: str
