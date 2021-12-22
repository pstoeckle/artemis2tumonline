"""
TUM Online Typing.
"""
from collections import Mapping
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

    @staticmethod
    def create_tum_online_entry(m: Mapping[str, str]) -> "TumOnlineEntry":
        """

        :param m:
        :return:
        """
        return TumOnlineEntry(
            registration_number=m["REGISTRATION_NUMBER"],
            number_of_the_course=m["Number_Of_The_Course"],
            date_of_assessment=m["DATE_OF_ASSESSMENT"],
            remark="",  # PS: Ignore this Field!
            ects_grade=m["ECTS_GRADE"],
            db_primary_key_of_candidate=m["DB_Primary_Key_Of_Candidate"],
            db_primary_key_of_exam=m["DB_Primary_Key_Of_Exam"],
        )


@dataclass(frozen=True)
class TumOnlineEntryWithGrade(TumOnlineEntry):
    """
    An Entry of the TUMOnline CSV with the grade.
    """

    grade: str
