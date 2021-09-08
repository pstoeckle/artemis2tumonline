# Artemis2TUMOnline

After conducting an exam with [Artemis](https://artemis.ase.in.tum.de/), you can download a CSV file with the grades of the students.
The problem is that the format of the Artemis export is **NOT** the format that TUMOnline is expecting.
Thus, you cannot directly upload the CSV to TUMOnline.

This small tool can help you to create the CSV for TUMOnline.

## Installation

```bash
poetry install
```

## Usage

```
poetry run artemis2tumonline --help
Usage: artemis2tumonline [OPTIONS]

  Reads a TUMOnline registration and a Artemis export file. Creates an
  TUMOnline file with the grades of the students.

Options:
  -t, --tumonline_registration_file FILE
  -a, --artemis_export_file FILE
  -o, --output_file FILE          [default: /path/to/cwd/tumonline.csv]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
 
```

### Example 

```bash
$ poetry run artemis2tumonline --tumonline_registration_file ./test/Modulpruefung_29072021-0800_IN2178_FA_SecurityEngineering.csv --artemis_export_file test/Final_exam__Security_EngineeringResults.csv
We load the TUM online file /path/to/cwd/test/Modulpruefung_29072021-0800_IN217 8_FA_SecurityEngineering.csv
... and the Artemis file /path/to/cwd/test/Final_exam__Security_EngineeringResults.csv
... and write the results in /path/to/cwd/tumonline.csv
```

## Misc

If you have any question, just write [me](mailto:patrick.stoeckle@tum.de?subject=Artemis2TUMOnline) an email.
