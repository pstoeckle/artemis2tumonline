# Artemis2TUMOnline

After conducting an exam with [Artemis](https://artemis.ase.in.tum.de/), you can download a CSV file with the grades of the students.
The problem is that the format of the Artemis export is **NOT** the format that TUMOnline is expecting.
Thus, you cannot directly upload the CSV to TUMOnline.

This small tool can help you to create the CSV for TUMOnline.

## Installation

The easiest way to install the package is to use pip.

```bash
pip install artemis2tumonline
```
**Attention**: On macOS, `pip` is usually the installer of the Python2 instance.
Please use `pip3` or `pip3.x` in this case.

If you want to work on the software, you can install the dependencies via [poetry](https://python-poetry.org/).

```bash
poetry install
```

## Usage

```bash
artemis2tumonline create-final-results --help
Usage: artemis2tumonline create-final-results [OPTIONS]

  Reads a TUMOnline registration and a Artemis export file. Creates an
  TUMOnline file with the grades of the students.

Options:
  -t, --tumonline-registration-file FILE
                                  The registration file. You can get this file
                                  from TUMOnline. Usually, this is the same
                                  file you use to register the students for
                                  the exam.
  -a, --artemis-export-file FILE  The CSV file you can download from Artemis.
  -o, --output-file FILE          The resulting CSV file. This file contains
                                  the necessary information from the TUMOnline
                                  Registration file and the grades from the
                                  Artemis export. You can upload this file to
                                  TUM Online.  [default: /path/to/cwd/tumonline.csv]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

```

### Example

```bash
$ poetry run artemis2tumonline --tumonline-registration-file ./test/Modulpruefung_29072021-0800_IN2178_FA_SecurityEngineering.csv --artemis-export-file test/Final_exam__Security_EngineeringResults.csv
We load the TUM online file /path/to/cwd/test/Modulpruefung_29072021-0800_IN217 8_FA_SecurityEngineering.csv
... and the Artemis file /path/to/cwd/test/Final_exam__Security_EngineeringResults.csv
... and write the results in /path/to/cwd/tumonline.csv
```

## Misc

If you have any question, just write [me](mailto:patrick.stoeckle@tum.de?subject=Artemis2TUMOnline) an email.
