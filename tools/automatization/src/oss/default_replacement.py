class MultiSpdxReplacement:
    def __init__(self, start, end, replace):
        self.data = {"start": start, "end": end, "replace": replace}


Default_TXT_Replacements_Single = {
    " MAIN LICENSES": "LICENSES",
    " OTHER LICENSES": "LICENSES",
}


Default_SPDX_Replacements_Single = {
    "^LicenseInfoInFile: LicenseRef-fossology-gpl-2.0-plus\n$": "",
    "^Creator: Person: .*()$": "Creator: Person: [CreatorName]",
    "^PackageLicenseConcluded: .*\n$": "PackageLicenseConcluded: NOASSERTION\n",
    "^This document was created using license information and a generator from Fossology.": 'This document was created using license information and a generator from Fossology.\nIt contains the license and copyright analysis of [package].\nPlease check "LicenseComments" for explanations of concluded licenses.',
}


Default_TXT_Replacements_Multi = []


Default_SPDX_Replacements_Multi = [
    vars(MultiSpdxReplacement("^LicenseID: LicenseRef-fossology-gpl-2.0-plus", "</text>\n$",""))["data"],
    #vars(MultiSpdxReplacement("^LicenseID: LicenseRef-CC0-1.0",  "</text>\n$",""))["data"],
]
