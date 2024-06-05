from oss.file_operation.file_parser import FileParser
from oss.utils.command_line_parser import parser
from packageurl.contrib import url2purl
from oss.content_analyzer.read_regex_replacement import ReadRegexReplacement


parser.add_argument(
    "-dl",
    "--download_link",
    required=False,
    type=str,
    help="The download link that it should be written in readme.",
)
parser.add_argument(
    "-r",
    "--reviewer",
    required=False,
    type=str,
    help="The reviewer that it should be written in readme.",
)


Dual_license_header = "\n## Comment\n\n"
Dual_license_comment = "This package is dual licensed under [selected_license] OR [second_license]. To facilitate automatic use, a default license choice of [selected_license] is denoted in the Acknowledgment section of the OSS disclosure document. This shall not restrict the freedom of users to choose either [selected_license] OR [second_license]. For convenience all license texts are provided.\n\n"


class ReadmeParser(FileParser):
    """This is a simple parser class that it parse and replace text in README.md file"""
    def __init__(
        self,
        file_path=None,
        dictionary_replacement_texts=None,
        ml_list_replacement_texts=None,
    ):
        FileParser.__init__(
            self, file_path, dictionary_replacement_texts, ml_list_replacement_texts
        )
        self.dual_license = ReadRegexReplacement.get_text_and_replacement_from_cmd(
            parser["dual_license_comment"]
        )

    def new_file_name_provider(self):
        return "README.md"

    def generate_purl(self):
        if parser["download_link"]:
            package_purl = url2purl.get_purl(parser["download_link"])
            print("PURL Link:   ", package_purl)
            if package_purl:
                return package_purl.to_string()

    def add_dual_license_comment(self, lines):
        if self.dual_license:
            lines.append(Dual_license_header)
            for key, value in self.dual_license.items():
                line = Dual_license_comment
                replacement_line = line.replace("[selected_license]", key)
                replacement_line = replacement_line.replace("[second_license]", value)
                lines.append(replacement_line)
        return lines

    def post_processing_operation(self, lines):
        new_line_list = []
        package_purl = self.generate_purl()
        for line in lines:
            replacement_line = line
            if "[CreatorName]" in line:
                replacement_line = line.replace("[CreatorName]", parser["creator_name"])
            elif "[DownloadLink]" in line:
                if parser["download_link"]:
                    replacement_line = line.replace(
                        "[DownloadLink]", parser["download_link"]
                    )
            elif "[PurlLink]" in line:
                if package_purl:
                    replacement_line = line.replace("[PurlLink]", package_purl)
            elif "[Reviewer]" in line:
                if parser["reviewer"]:
                    replacement_line = line.replace("[Reviewer]", parser["reviewer"])
            new_line_list.append(replacement_line)
        return new_line_list

    def final_processing(self, lines):
        return self.add_dual_license_comment(lines)
