class MultiReplacement:
    def __init__(self, start, end, replace):
        self.data = {"start": start, "end": end, "replace": replace}


Default_TXT_Replacements_Single = {
    " MAIN LICENSES": "LICENSES",
    " OTHER LICENSES": "LICENSES",
}


Default_SPDX_Replacements_Single = {
    #"^LicenseInfoInFile: LicenseRef-fossology-gpl-2.0-plus\n$": "",
    "^Creator: Person: .*()$": "Creator: Person: [CreatorName]",
    "^PackageLicenseConcluded: .*\n$": "PackageLicenseConcluded: NOASSERTION\n",
    "^This document was created using license information and a generator from Fossology.": 'This document was created using license information and a generator from Fossology.\nIt contains the license and copyright analysis of [package].\nPlease check "LicenseComments" for explanations of concluded licenses.',
}


Default_TXT_Replacements_Multi = [
    vars(MultiReplacement("^NOASSERTION", "\n$",""))["data"],
]

# Per default, we do not replace any LicenseID. This feature is in testing phase and it can be activated.
# However, it needs extra caution.
Default_SPDX_Replacements_Multi = [
    #vars(MultiReplacement("^LicenseID: LicenseRef-fossology-gpl-2.0-plus", "</text>\n$",""))["data"],
    #vars(MultiReplacement("^LicenseID: LicenseRef-CC0-1.0",  "</text>\n$",""))["data"],
]
