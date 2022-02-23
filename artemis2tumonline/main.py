"""
Main.
"""

from csv import DictReader, DictWriter
from dataclasses import asdict
from logging import INFO, basicConfig, getLogger
from pathlib import Path
from typing import List, MutableSet

from artemis2tumonline import __version__
from artemis2tumonline.model.artemis_entry import ArtemisEntry
from artemis2tumonline.model.tum_online_entry import (TumOnlineEntry,
                                                      TumOnlineEntryWithGrade)
from typer import Exit, Option, Typer, echo, style
from typer.colors import RED


def error_echo(s: str) -> None:
    """

    :param s:
    :return:
    """
    echo(style(s, fg=RED), err=True)


_LOGGER = getLogger(__name__)
basicConfig(
    format="%(levelname)s: %(asctime)s: %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=INFO,
    filename="artemis2tumonline.log",
    filemode="w",
)


def _version_callback(value: bool) -> None:
    if value:
        echo(f"artemis2tumonline {__version__}")
        raise Exit()


app = Typer()


@app.callback()
def _call_back(
    _: bool = Option(
        None,
        "--version",
        is_flag=True,
        callback=_version_callback,
        expose_value=False,
        is_eager=True,
        help="Version",
    )
) -> None:
    """

    :return:
    """


@app.command()
def create_final_results(
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
        _LOGGER.info(f"Handling {entry}")
        thing_to_add: TumOnlineEntryWithGrade
        try:
            artemis_entry = next(
                a
                for a in artemis_entries
                if a.matriculation_number == entry.registration_number
            )
            _LOGGER.info(f"... and {artemis_entry}")
            thing_to_add = TumOnlineEntryWithGrade(
                grade=(
                    artemis_entry.overall_grade if artemis_entry.submitted else "X-5.0"
                ),
                **asdict(entry),
            )
        except StopIteration:
            _LOGGER.info(f"We could not find a matching entry for {entry}")
            _LOGGER.info("Maybe the matriculation number was interpreted as int ...")
            try:
                artemis_entry = next(
                    a
                    for a in artemis_entries
                    if int(a.matriculation_number) == int(entry.registration_number)
                )
                _LOGGER.info(f"... and {artemis_entry}")
            except StopIteration:
                _LOGGER.error("... and this was also not working...")
                echo(f"We could not find a matching entry for {entry}")
                raise Exit(1)
            entry_dict = asdict(entry)
            del entry_dict["registration_number"]
            thing_to_add = TumOnlineEntryWithGrade(
                grade=(
                    artemis_entry.overall_grade if artemis_entry.submitted else "X-5.0"
                ),
                registration_number=artemis_entry.matriculation_number,
                **entry_dict,
            )

        artemis_entries.remove(artemis_entry)
        entries_with_grades.append(thing_to_add)

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
