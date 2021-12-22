"""
Main.
"""

from csv import DictReader, DictWriter
from dataclasses import asdict
from pathlib import Path
from typing import List, MutableSet

from artemis2tumonline.model.artemis_entry import ArtemisEntry
from artemis2tumonline.model.tum_online_entry import (
    TumOnlineEntry,
    TumOnlineEntryWithGrade,
)
from typer import Option, Typer, echo

app = Typer()


@app.command()
def artemis2tumonline(
    tumonline_registration_file: Path = Option(
        "",
        "--tumonline-registration-file",
        "-t",
        exists=True,
        dir_okay=False,
        resolve_path=True,
        help="The registration file. You can get this file from TUMOnline. Usually, this is the same file you use to register the students for the exam.",
    ),
    artemis_export_file: Path = Option(
        "",
        "--artemis-export-file",
        "-a",
        exists=True,
        dir_okay=False,
        resolve_path=True,
        help="The CSV file you can download from Artemis.",
    ),
    output_file: Path = Option(
        "tumonline.csv",
        "--output-file",
        "-o",
        dir_okay=False,
        writable=True,
        resolve_path=True,
        help="The resulting CSV file. This file contains the necessary information from the TUMOnline Registration file and the grades from the Artemis export. You can upload this file to TUM Online.",
    ),
) -> None:
    """
    Reads a TUMOnline registration and a Artemis export file.
    Creates an TUMOnline file with the grades of the students.
    """
    echo(f"We load the TUM online file {tumonline_registration_file}")
    echo(f"... and the Artemis file {artemis_export_file}")
    entries: List[TumOnlineEntry]
    artemis_entries: MutableSet[ArtemisEntry]
    with tumonline_registration_file.open(encoding="cp852") as f_file:
        reader = DictReader(f_file, delimiter=";")
        entries = [TumOnlineEntry.create_tum_online_entry(m) for m in reader]
    with artemis_export_file.open() as f_file:
        reader = DictReader(f_file, delimiter=";")
        artemis_entries = set(ArtemisEntry.create_artemis_entry(a) for a in reader)

    entries_with_grades: List[TumOnlineEntryWithGrade] = []

    for entry in entries:
        artemis_entry = next(
            a
            for a in artemis_entries
            if a.matriculation_number == entry.registration_number
        )
        artemis_entries.remove(artemis_entry)
        entries_with_grades.append(
            TumOnlineEntryWithGrade(
                grade=(
                    artemis_entry.overall_grade if artemis_entry.submitted else "X-5.0"
                ),
                **asdict(entry),
            )
        )

    if len(artemis_entries) > 0:
        for a in artemis_entries:
            echo(f"The following artemis entry was NOT part of the TUM Online CSV {a}")
        echo("Remember to inform these students separately about their grades!")

    echo(f"... and write the results in {output_file}")
    with output_file.open("w") as f_write:
        writer = DictWriter(
            f_write,
            [
                "registration_number",
                "number_of_the_course",
                "date_of_assessment",
                "grade",
                "remark",
                "ects_grade",
                "db_primary_key_of_candidate",
                "db_primary_key_of_exam",
            ],
            delimiter=";",
            lineterminator="\n",  # PS:Only \n is a valid terminator, not \r\n...
        )
        writer.writeheader()
        for e in entries_with_grades:
            writer.writerow(asdict(e))


if __name__ == "__main__":
    app()
