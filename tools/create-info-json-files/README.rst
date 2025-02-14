OSSelot Info File Generator
===========================

This script generates `info.json` files for OSSelot packages. It walks through specified package directories, collects package information, and creates JSON files.

Installation
------------

The script was created and tested with Python 3.11.

1. Create a virtual environment and activate it::

    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux

2. Install the required dependencies::

    pip install jsonschema

Dependencies
------------

The script requires the following (non standard) Python packages:

- `jsonschema` (https://pypi.org/project/jsonschema/)

Note
----

The file `info-schema.json` must be present inside the scripts directory.
This file contains the JSON schema against which the created `info.json` files are validated.

Usage
-----

Run the script with the following command::

    python create_info_json.py [OPTIONS]

Options
~~~~~~~

- `--overwrite`, `-o`: Overwrite existing `info.json` files if the flag is set.
- `--packages`, `-p`: Filter packages for which an `info.json` file should be created. (e.g., `--packages a*` will create it for all packages beginning with 'a').
- `--packages-dir`, `-d`: The directory containing the packages to analyze. Default is `../../analysed-packages`.

Example
~~~~~~~

To generate `info.json` files for all packages in the default directory::

    python create_info_json.py

To generate `info.json` files for packages starting with 'a' and overwrite existing files::

    python create_info_json.py --packages a* --overwrite

Logging
-------

The script logs its output to both a file (`osselot_info_file_gen.log`) and the terminal. The log file is created in the same directory as the script.

License
-------

All the files in this directory are licensed under CC0-1.0