"""
SPDX-License-Identifier: CC0-1.0

This script generates information files for OSSelot packages.
The script walks through all specified packages in a given directory and creates 'info.json'
files containing package information.
It extracts package details from README files and other relevant files within each package directory.

Usage:
    Run the script with the following command line arguments:
    - --overwrite, -o: Overwrite existing info.json file for packages if the flag is set.
    - --packages, -p: Filter packages for which an "info.json" file should be created.
    - --packages-dir, -d: The directory containing the packages to analyze. Default is '../../analysed-packages'.

Example:
    python create_info_json.py --overwrite --packages "a*" --packages-dir "/path/to/packages

Copyright (c) 2024 Vaillant GmbH. All rights reserved.

Author: andreas.menzl.ext@vaillant-group.com
"""

import json
import logging
import os
import re
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict

import jsonschema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("osselot_info_file_gen.log")
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


class OsselotInfoFileGen:
    """Class to generator info files for OSSelot packages."""

    def __init__(self, args):
        """
        Initializes the OsselotInfoFileGen object.

        Args:
        - args: The command line arguments.

        Attributes:
        - _args: The command line arguments.
        """
        self._packages_dir = Path(args.packages_dir)
        self._args = args

    def generate_info_files(self):
        """
        Generates information files for OSSelot packages.
        Walks through all specified packages to generate the necessary information files.

        Raises:
            Exception: If an error occurs during the generation of information files.
        """
        if not self._packages_dir.exists():
            logger.error("The specified packages directory does not exist: %s", self._packages_dir)
            return

        logger.info("Starting to create 'info.json' files for OSSelot packages.")
        try:
            self.walk_all_packages(self._args.packages)
        except Exception:  # pylint:disable=broad-exception-caught
            logger.exception("Error generating info file for OSSelot packages:")
        logger.info("Finished creating 'info.json' files for OSSelot packages.")

    def walk_all_packages(self, filter: str | None = None):
        """
        Walk through all packages in the specified directory and create 'info.json' files for OSSelot packages.

        Args:
            filter (str | None): An optional filter to determine which packages should have 'info.json' files created.
        """
        logger.info("Walking through packages in directory: %s", self._packages_dir)
        for root, dirs, _ in os.walk(self._packages_dir):
            for directory in dirs:
                full_path = Path(root) / directory
                package_infos = self._collect_package_infos(full_path)

                if self._should_create_info_file(package_infos, filter):
                    self._create_info_file(full_path, package_infos)

    def _collect_package_infos(self, full_path: Path):
        """
        Collects package information from the given directory path.

        Args:
            full_path (Path): The full path to the package directory.

        Returns:
            dict: A dictionary containing package information.
        """
        relative_path = full_path.relative_to(self._packages_dir)
        package_infos: Dict[str, Any] = {
            "structure": relative_path.parts,
            "version": None,
            "clearing_files": {"fileName": "", "priority": "n/a", "author": "", "reviewer": [], "alternate_files": []},
            "download_url": None,
            "package_name": None,
            "comment": None,
        }

        for file in full_path.iterdir():
            if file.name.endswith(".rdf.xml"):
                package_infos["clearing_files"]["fileName"] = file.name
            elif "spdx" in file.name:
                package_infos["clearing_files"]["alternate_files"].append({"fileName": file.name})
            elif file.name == "README.md":
                parent_folder = file.parent.name.lower()
                version = parent_folder.replace("version-", "") if "version" in parent_folder else parent_folder

                package = self._get_package_infos_from_readme(file)
                if package.get("download_url"):
                    package_name = (
                        "_".join(package_infos["structure"][0:-1])
                        if len(package_infos["structure"]) > 2
                        else package_infos["structure"][0] if package_infos["structure"] else None
                    )
                    package_infos["clearing_files"].update(
                        {"author": package["author"], "reviewer": package["reviewer"]}
                    )
                    package_infos.update(
                        {
                            "version": version,
                            "download_url": package["download_url"],
                            "package_name": package_name,
                            "comment": package["comment"],
                        }
                    )

        return package_infos

    def _should_create_info_file(self, package_infos: dict, filter: str | None):
        """
        Determines whether an info file should be created based on the provided package information and filter.

        Args:
            package_infos (dict): A dictionary containing package information.
            filter (str | None): An optional filter string to match the package name against. If None, no filtering is applied.

        Returns:
            bool: True if the info file should be created, False otherwise.
        """
        return (
            package_infos["download_url"]
            and package_infos["package_name"]
            and (not filter or self._wildcard_search(filter, package_infos["package_name"]))
        )

    def _create_info_file(self, full_path: Path, package_infos: dict):
        """
        Creates an info.json file with the provided package information.

        Args:
            full_path (Path): The directory path where the info.json file will be created.
            package_infos (dict): A dictionary containing package information.
        """
        data = {
            "name": package_infos["package_name"],
            "version": package_infos["version"],
            "description": "",
            "comment": package_infos["comment"],
            "src": {"tarball": {"url": package_infos["download_url"]}},
            "clearingFiles": [package_infos["clearing_files"]],
        }
        info_json_file = full_path / "info.json"
        self._create_info_json(data, info_json_file)

    @staticmethod
    def _get_package_infos_from_readme(file: Path):
        """
        Extracts package information from a readme file.

        Args:
            file (Path): The path to the readme file.

        Returns:
            dict: A dictionary containing the package information.
        """
        package = {"download_url": "", "author": "", "comment": "", "reviewer": []}
        with file.open(mode="r") as readme:
            content = readme.read()

            download_url_match = re.search(r"## Download Location\n\n(.+)", content)
            if download_url_match:
                package["download_url"] = download_url_match.group(1).strip()

            author_match = re.search(r"## Creator\n\n(.+)", content)
            if author_match:
                package["author"] = author_match.group(1).strip()

            comment_match = re.search(r"## Comment\n\n(.+)", content)
            if comment_match:
                package["comment"] = comment_match.group(1).strip()

            reviewer_section_match = re.search(
                r"## Reviewers\n\nThe information was reviewed by:\n\n(.+)", content, re.DOTALL
            )
            if reviewer_section_match:
                section_content = reviewer_section_match.group(1)
                # Find all lines starting with "*"
                reviewer_match = re.findall(r"^\* (.+)$", section_content, re.MULTILINE)
                if reviewer_match:
                    reviewer = [
                        reviewer.strip()
                        for reviewer in reviewer_match
                        if reviewer.strip().lower() != "add reviewer here"
                    ]
                    package["reviewer"] = reviewer

        return package

    @staticmethod
    def _wildcard_search(pattern: str, text: str):
        """
        Perform a wildcard search on the given text using the specified pattern.

        Args:
            pattern (str): The pattern to search for, which can include wildcards (*).
            text (str): The text to search within.

        Returns:
            bool: True if the text matches the pattern, False otherwise.
        """
        if pattern.startswith("*") and pattern.endswith("*"):
            return pattern[1:-1] in text
        if pattern.startswith("*"):
            return text.endswith(pattern[1:])
        if pattern.endswith("*"):
            return text.startswith(pattern[:-1])
        return text == pattern

    def _create_info_json(self, data: dict, output_file: Path):
        """
        Creates a JSON file from the provided data dictionary and validates it against a JSON schema.

        Args:
            data (dict): The data to be written to the JSON file.
            output_file (str): The path where the JSON file will be created.

        Raises:
            jsonschema.exceptions.ValidationError: If the data does not conform to the JSON schema.
        """
        try:
            if not self._args.overwrite and output_file.is_file():
                logger.info("Skip info file creation for %s: Already exists and --overwrite arg not set", output_file)
                return

            info_json_schema_path = Path("info-schema.json")
            if not info_json_schema_path.exists():
                logger.error("JSON schema file not found at: %s", info_json_schema_path)
                return

            with open(info_json_schema_path, "r", encoding="utf8") as schema_file:
                schema = json.load(schema_file)

            info_json_content = {"schema_version": schema["version"]}
            info_json_content.update(data)
            jsonschema.validate(instance=info_json_content, schema=schema)

            with open(output_file, "w", encoding="utf8") as f:
                json.dump(info_json_content, f, indent=4)

            logger.info("info.json file created successfully at %s", output_file)
        except jsonschema.exceptions.ValidationError:
            logger.exception("Data validation error while validating json schema for %s", output_file)


def main():
    """Main function to parse command-line arguments and generate info.json files for packages."""
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "--overwrite",
        "-o",
        action="store_true",
        help="Overwrite existing info.json file for packages if the flag is set.",
    )
    arg_parser.add_argument(
        "--packages",
        "-p",
        help='Filter packages for which a "info.json" file should be created. (e.g. "--packages a*" will import all packages beginning with a)',
    )
    arg_parser.add_argument(
        "--packages-dir",
        "-d",
        default="../../analysed-packages",
        help="The directory containing the packages to analyze. Default is '../../analysed-packages'.",
    )

    args = arg_parser.parse_args()
    osselot_info_file_gen = OsselotInfoFileGen(args)
    osselot_info_file_gen.generate_info_files()


if __name__ == "__main__":
    main()
