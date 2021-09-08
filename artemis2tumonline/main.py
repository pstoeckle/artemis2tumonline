"""
Main.
"""

from csv import DictReader, DictWriter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Mapping

from typer import Option, Typer, echo

app = Typer()


@dataclass(frozen=True)
class ArtemisEntry(object):
    matriculation_number: str
    overal_grade: str
    submitted: bool


@dataclass(frozen=True)
class TumOnlineEntry(object):
    registration_number: str
    number_of_the_course: str
    date_of_assessment: str
    remark: str
    ects_grade: str
    db_primary_key_of_candidate: str
    db_primary_key_of_exam: str

    def create_entry_with_grade(self, artemis_entries: List[ArtemisEntry]) -> "TumOnlineEntryWithGrade":
        artemis_entry = next(a for a in artemis_entries if a.matriculation_number == self.registration_number)
        grade: str = artemis_entry.overal_grade if artemis_entry.submitted else "X-5.0"

        return TumOnlineEntryWithGrade(
                grade=grade,
                **asdict(self)
        )


@dataclass(frozen=True)
class TumOnlineEntryWithGrade(TumOnlineEntry):
    grade: str


def create_tum_online_entry(m: Mapping[str, str]) -> TumOnlineEntry:
    return TumOnlineEntry(
            registration_number=m["REGISTRATION_NUMBER"],
            number_of_the_course=m["Number_Of_The_Course"],
            date_of_assessment=m["DATE_OF_ASSESSMENT"],
            remark="",  # PS: Ignore this Field!
            ects_grade=m["ECTS_GRADE"],
            db_primary_key_of_candidate=m["DB_Primary_Key_Of_Candidate"],
            db_primary_key_of_exam=m["DB_Primary_Key_Of_Exam"]
    )


def create_artemis_entry(m: Mapping[str, str]) -> ArtemisEntry:
    return ArtemisEntry(
            matriculation_number=m["Matriculation Number"],
            overal_grade=m["Overall Grade"],
            submitted=(m["Submitted"] == "yes")
    )


@app.command()
def artemis2tumonline(
        tumonline_registration_file: Path = Option("", "--tumonline_registration_file", "-t", exists=True,
                                                   dir_okay=False, resolve_path=True),
        artemis_export_file: Path = Option("", "--artemis_export_file", "-a", exists=True, dir_okay=False,
                                           resolve_path=True),
        output_file: Path = Option("tumonline.csv", "--output_file", "-o", dir_okay=False, writable=True,
                                   resolve_path=True)
) -> None:
    echo(f"We load the TUM online file {tumonline_registration_file}")
    echo(f"... and the Artemis file {artemis_export_file}")
    entries: List[TumOnlineEntry]
    artemis_entries: List[ArtemisEntry]
    with tumonline_registration_file.open(encoding='cp852') as f_file:
        reader = DictReader(f_file, delimiter=";")
        entries = [create_tum_online_entry(m) for m in reader]
    with artemis_export_file.open() as f_file:
        reader = DictReader(f_file, delimiter=";")
        artemis_entries = [create_artemis_entry(a) for a in reader]
    entries_with_grades = [e.create_entry_with_grade(artemis_entries) for e in entries]
    for entry in entries_with_grades:
        echo(entry)
    echo(f"... and write the results in {output_file}")
    with output_file.open('w') as f_write:
        writer = DictWriter(f_write,
                            ["registration_number", "number_of_the_course", "date_of_assessment", "grade", "remark",
                             "ects_grade", "db_primary_key_of_candidate", "db_primary_key_of_exam"], delimiter=";")
        writer.writeheader()
        for e in entries_with_grades:
            writer.writerow(asdict(e))


if __name__ == '__main__':
    app()
