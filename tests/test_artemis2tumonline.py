"""
Test the basic behavior.
"""
from csv import DictReader
from os import remove
from pathlib import Path
from unittest import TestCase, main as unit_main

from typer.testing import CliRunner

from artemis2tumonline.main import app


class BasicTest(TestCase):
    """
    A basic test.
    """
    runner: CliRunner
    output_file = Path("tumonline.csv")

    @classmethod
    def setUpClass(cls) -> None:
        """
        Test.
        :return:
        """
        cls.runner = CliRunner()

    def tearDown(self) -> None:
        """
        Remove test files.
        :return:
        """
        if self.output_file.exists():
            remove(self.output_file)

    def test_normal(self) -> None:
        """
        Test normal behavior.
        :return:
        """
        result = self.runner.invoke(app, ["--tumonline-registration-file", "tests/rsc/test_registration_file.csv",
                                          "--artemis-export-file", "tests/rsc/test_artemis_export.csv"])
        self.assertEqual(result.exit_code, 0, msg=result.stdout)

        self.assertTrue(self.output_file.exists(), msg="There was no CSV file created.")
        with self.output_file.open() as f_read:
            lines = f_read.readlines()
            for line in lines:
                self.assertTrue(line.endswith('\n'))
                self.assertFalse(line.endswith('\r\n'))

        with self.output_file.open() as f_read:
            reader = DictReader(f_read, delimiter=";")
            entries = list(reader)
        self.assertEqual(entries[0]["registration_number"], "123")
        self.assertEqual(entries[1]["registration_number"], "12")
        self.assertEqual(entries[2]["registration_number"], "1")

        self.assertEqual(entries[0]["grade"], "X-5.0")
        self.assertEqual(entries[1]["grade"], "5.0")
        self.assertEqual(entries[2]["grade"], "1.0")

        self.assertEqual(entries[0]["db_primary_key_of_candidate"], "222")
        self.assertEqual(entries[1]["db_primary_key_of_candidate"], "555")
        self.assertEqual(entries[2]["db_primary_key_of_candidate"], "888")

        for i in range(2):
            self.assertEqual(entries[i]["number_of_the_course"], "IN2178")
            self.assertEqual(entries[i]["date_of_assessment"], "1.01.1900")
            self.assertEqual(entries[i]["remark"], "")
            self.assertEqual(entries[i]["ects_grade"], "")

    def test_no_artemis_entry(self) -> None:
        self.assertFalse(self.output_file.exists())
        result = self.runner.invoke(app, ["--tumonline-registration-file", "tests/rsc/test_missing_id.csv",
                                          "--artemis-export-file", "tests/rsc/test_artemis_export.csv"])
        self.assertEqual(result.exit_code, 1)
        self.assertIsInstance(result.exception, StopIteration)
        self.assertFalse(self.output_file.exists(), msg="There was")


if __name__ == '__main__':
    unit_main()
