"""
Artemis Typing.
"""
from collections import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class ArtemisEntry(object):
    """
    An entry in the export file coming from Artemis.
    """

    matriculation_number: str
    overall_grade: str
    submitted: bool
    login: str

    @staticmethod
    def create_artemis_entry(m: Mapping[str, str]) -> "ArtemisEntry":
        """
        
        :param m:
        :return:
        """
        return ArtemisEntry(
            matriculation_number=m["Matriculation Number"],
            overall_grade=m["Overall Grade"],
            submitted=(m["Submitted"] == "yes"),
            login=m["Login"],
        )
