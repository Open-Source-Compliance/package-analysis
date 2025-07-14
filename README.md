# package-analysis
This repo contains license and copyright analysis results of open source packages. 

The objective of the project is to lower the required effort for all who want to make use of OSS in a license compliant way. 

To achieve this we will develop, share and improve the artifacts commonly used to fulfill the requirements of the different Free and Open Source Software licenses by applying the Open Source Software development principles. This may turn Open Source license compliance into a straight forward task. 

Another objective is a very close collaboration with the OSS community in order to fix detected "bugs" in licensing as well as introducing the information needed for license compliance activities in the Open Source projects, i.e. provide our analysis work to the OSS projects.

One of the tasks in OSS compliance work is the analysis of OSS packages in order to identify the licenses and copyright holders. Although tools are available which support the analysis, it is still the task which causes effort.
We believe that is does not make any sense that everyone doing checks of packages again and again. This is redundant effort in our opinion which could be much better invested in OSS development. In other words: we think increasing the code base is much better instead of spending effort for license compliance checks which are done thousand fold today in many different organizations.

You can also visit our [website](https://www.osselot.org/index.php)

In case you want to use the artifacts in a more automated way we provide also a state of the art [REST API](https://wiki.osselot.org/index.php/REST)

## Provided artifacts

The analysis results are provided in the "analysed-packages" directory. Usually two artifacts are provided - a SPDX tag-value file and a ready to use OSS-disclosure file. The main difference between both is that the tag-value files can be used and integrated in the build process in a way that only the licenses of those files are considered which will end up in the build artifact. Furthermore the tag-value files contain notes on license conclusions to make decisions transparent if necessary. The OSS-disclosure files contain all applicable licenses and all copyright notices of the entire package. Additionally to this the OSS-disclosure files contain "acknowledgment texts" if such an acknowledgment is required by the license.

## Process we follow in order to create a OSS package analysis file
We create such OSS package analysis files and make them available for download under the terms of the Creative Commons Public Domain Dedication [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/). We know that the content we produce is somehow delicate. Due to this it is important to disclose how we create such content. Since we represent an Open Source project everything is transparent. The following points describe the procedure we follow in creating the "OSS package analysis file" as we call it. 

The OSS package analysis file are generated following the process described below:

* Obtain the component in source code form
	* download the component - we provide the link were we downloaded the component in the corresponding README file.
	* the download URL is provided in the README files of the corresponding directories
	* additionally to the download url the corresponding package URL is provided in the README files
* Issue a license and copyright analysis with the GPL-2.0 licensed tool [FOSSology](https://www.fossology.org/). 
For license and copyright statement identification FOSSology provides different "agents" the user is able to select, which "agents" shall run, currently the following "agents" are available:
	* Nomos
	* Monk
	* Ojo
	* Scancode (currently not on all packages)
  
  Each agent was build with a different main focus and we think that running them combined produces the best output. Which agents were run for a concrete package analysis is available in the SPDX2TV file.

* A licensing expert person will review and analyze the FOSSology result. The expert person is not necessarily a lawyer, but has several years of experience in license compliance activities.


We do an analysis of the entire package on file level. This means that all files are analyzed, no matter whether they end up in the produced binaries, if there will be some, or not. This includes potentially available "test" and/or "documentation" or other directories. We do this because we do not know what you or others will exactly build. For example the Linux kernel can be build for many different platforms, with many different file systems and so on, if we would analyze only the "ARM" tree the analysis would be of no value for users with other platforms.

### License identification and conclusion

As already explained in the overall process description a licensing expert will review the scanner findings. During the review depending on the scanner matches, the corresponding text sections and the context in the files the following tasks are carried out:
* confirm scanner findings either file by file or via bulk statement
* correct scanner findings either file by file or via bulk statement

The following subsections provide more information about the tasks carried out:

#### Correcting scanner findings
There might be cases where the scanner matches some license information in a file but this information is not the license of the file. For example
> "DT binding documents should be licensed (GPL-2.0-only OR BSD-2-Clause)\n" . $herecurr) && $fix) {$fixed[$fixlinenr] =~ s/SPDX-License-Identifier: .*/SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)/;

This is some code checking whether some files carry the expected SPDX expressions, thus it is not the licensing of this particular file. In this case and due to the fact that the file does not contain any license information the conclusion is "no license known", which is mapped to "NOASSERTION" in SPDX terminology.

There might be cases where in a Readme file of the subdirectory or on root level of the package there is a statement, like:
> Files in directory abc are all licensed under Apache-2.0 

This is an, of course, unwanted situation, because this kind of information tends to get outdated, because it is disconnected from the files located in the directory. 
The main problem is, if we would per default "assign" the license mentioned to all these files, we might do an unauthorized "licensing". Currenty we document this, but we do not conclude the license mentioned for the files. 

A different case is a file containing information of licenses of files, which do not include any license information like font files or pictures. In case we find such a reference in the package, be it in the README in the root directory or in a README in the specific directory or a file with similar content but another name, we check whether the named files (if the files are listed by name) are still present. Furthermore we check the internet whether the presented information is correct, in case this is possible. Finally we conclude the mentioned and if possible the in the internet verified licenses for the identified files. 

In both and similar cases usually we provide an explanation, why the scanner findings where corrected via "LicenseConcluded". This explanation is available in the SPDX2TV files as value of the tag "LicenseComments". In the above mentioned example the explanation is:
> The information in the file is:
>
> "DT binding documents should be licensed (GPL-2.0-only OR BSD-2-Clause)\n" . $herecurr) && $fix) {$fixed[$fixlinenr] =~ s/SPDX-License-Identifier: .*/SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)/;
>
> This is perl code checking whether some files carry the expected SPDX expressions, thus it is not the licensing of this particular file.

Please note that currently FOSSology maps the license conclusion "irrelevant" to "NOASSERTION". Furthermore there are currently no LicenseComments copied into the SPDX2TV files although they were provided during the review of the scanner matches.

#### Confirming scanner findings
In cases where the scanner matches are correct, we confirm the matches. This is outlined in the SPDX2TV files in the tag "LicenseConcluded".

We do not provide in the "LicenseComments" "standard" boilerplates, like:
>  Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
>
>    http:www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License.

Because in these cases the confirmation of the scanner findings are straight forward and providing the "obvious" might cover the important things.

#### Render scanner findings more precisely

There are cases where the scanners match BSD license (or other licenses), like BSD-3-Clause but the concrete license text is "individualized", like:

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer as
   the first lines of this file unmodified.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY **Andy Polyakov** ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL **NTT** BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

In these cases we conclude the correct class of the license (BSD-2-Clause in this case) where ever possible **and** provide the concrete individualized license text. 

#### External references

Sometimes we find statements like this:

> BSD 2-Clause License (http://www.opensource.org/licenses/bsd-license.php)

We then check the link, whether it is broken or not and still provides usefull information, if possible we take year information into account. We provide the result of the investigation as the value of "LicenseComments" tag including the date when the information was retrieved, like this: 

> The information in the file is:
> 
> BSD 2-Clause License (http://www.opensource.org/licenses/bsd-license.php)
> 
> visiting the internet link, displayed the following text. The link was visited on 20th of June 2022:
> 
> Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
> 
> 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
> 
> 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
> 
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
> 
> The link was visited on 20th of June 2022

#### No scanner findings
There might be files, which carry no license information and there is no hint of the applicable license in any other file of the package. Here the conclusion then is "no license known" ("NO ASSERTION"). We do not "assign" the license which might be available in the root directory to those file, because we cannot be sure whether this is the correct license.

#### The license files itself
In many cases there are files named LICENSE.txt or COPYING or similar in the root or subordinate directories of a package. These files usually contain the license text, e.g. the text of the GPL-2.0. Determining the license of these file is easy for the licenses of the GNU project, because they carry an explicit license statement:

>  Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

For most of the other license texts no license exist, like for BSD-3-Clause, MIT etc. Usually all scanners fail when it comes to license files. They match the content of the file, like GPL-2.0 but this is **not** the license of the file. In these cases usually the scanner matches are concluded as irrelevant, which translates to **NOASSERTION** in SPDX terminology, in case of the GNU licenses the correct license is concluded.

This might in some cases lead to strange analysis results, especially when the analysed package only contains a LICENSE.txt file with the license text and no reference to it in the other files. We are aware of this and try to make this transparent either in the LicenseComments or in the CreatorComment in the SDPX files.

Recently we decided to act in those cases as follows:
If there is on root level a LICENSE.txt or COPYING or similar file we conclude this as "main license" (i.e. clicking on the star in the "Action" column of the license table in the file view of FOSSology) **and** concluding the license information as irrelevant. This procedure ensures that in the SPDX tag-value files the Attributes "PackageLicenseConcluded" and "PackageLicenseDeclared" are set and the specific file (i.e. LICENSE.txt or other) has LicenseConcluded = "NOASSERTION".

Example:
The LICENSE.txt file on root level contains the text of the MIT license. With the above explained procedure this will result in: 
> PackageLicenseConcluded: MIT

> PackageLicenseDeclared: MIT

> ...

> FileName: pacakge-abc/LICENSE

> ...

>LicenseConcluded: NOASSERTION

> ...

> LicenseInfoInFile: MIT

#### Packages with "THIRD-PARTY-NOTICE" files
Some packages provide files in which they list the license of included software or software which is needed to run the built package. In most of the cases the files are called "THIRD-PARTY-NOTICE" or similar. According to our experience such files get/are outdated in most of the cases. We discussed with a lawyer how to treat the content of such files. The lawyer's statement was, that we should provide the content of such files unmodified in the created artifacts, although they might be outdated and/or incomplete. Based on this advice we follow currentl the below listed approach:
We provide the entire content of such files in the element "PackageLicenseComments:" in the SPDX file: 
>PackageLicenseComments: <text> licenseInfoInFile determined by Scanners:
> - nomos (abcd)
> - monk (abcd)
> - ojo (abcd)
> - scancode (abcd) 
>********************************************************************************
>Additional information found in: Python-3.10.8/Doc/license.rst
>
Licenses and Acknowledgments for Incorporated Software
>=======================================================

and in the discloure files right after the "LICENSES" section and before the "ACKNOWLEDGEMENT" section (if present):
>********************************************************************************
>
>Additional information found in: Python-3.10.8/Doc/license.rst
>
Licenses and Acknowledgements for Incorporated Software
>=======================================================

Please be aware that this strategy was not present in the beginning of the project.

### Copyright extraction

The copyright information of all files within the package is extracted, no matter in which directory the file is located. For files containing no copyright information no copyright information can be extracted. Sometimes it is necessary to "post process" the found copyright statements, this is done always when the copyright statements:
* contain some "clutter"
* are incomplete
* there is a statement like: "Copyright 1995-2022 The Project Authors, see AUTHORS for more detail" 
In these cases, we check whether there is a AUTHORS file in the package - if yes, then we add the content of the AUTHORS file to the extracted copyright statements, although we cannot be 100% sure whether the listed persons and/or organizations hold copyright on the package.

We do not check and extract committer information from the source code repos like GitHub because this information is even less accurate than the "AUTHORS" file approach. On GitHub the commit is done by an individual, but the holder of the copyright of this commit might be the organization the individual is working for.

## Audience
Everybody who has to deal with license compliance - legal persons, license compliance experts, product responsibles as well as developers and not to forget persons, who are in charge of the quality processes.

For the legal persons and the license compliance experts the OSS-disclosure text files are probably more interesting. Although the SPDX2TV files contain on file granularity the license information (identified and concluded licenses), the copyright information and if necessary information about the license conclusion to provide transparency about why the specific conclusion was made.

For the developers the SPDX2TV files will be most interesting, since they contain information about every file of the package. Developers can consume these files in the build pipelines. The files which are "used" to produce the to delivered software can be tracked and logged, with this information the SPDX2TV files can be parsed about the copyright and license information of those "used" files. This procedure will ensure that only the relevant licenses and copyright notices are extracted from the SPDX2TV files. 

Nevertheless the OSS-disclosure files are also of value for the developers, because they provide a very fast overview about the license situation of the entire package.

The information provided in the SPDX2TV files is complete in a way that it can be consumed. License as well as the copyright information can be extracted for every file, like:
> ##File
> 
> **FileName:** zephyr-2.7.2.tar.gz/zephyr-2.7.2.tar/zephyr-2.7.2/include/net/http_parser_state.h
> 
> SPDXID: SPDXRef-item155522901
> 
> FileChecksum: SHA1: f945f540e665d298c5e7eaa96f55964e128e95b0
> 
> FileChecksum: SHA256: 9ea05f8dd5e9cec4a76e105a96e2ef1c9a092b805ffaad5ce8cc64b521bef157
> 
> FileChecksum: MD5: b035f7f65e3fe28473adda750793afae
> 
> **LicenseConcluded:** LicenseRef-MIT
> 
> LicenseComments: <text>NOASSERTION </text>
> 
> LicenseInfoInFile: LicenseRef-MIT
> 
> **FileCopyrightText:** <text> Copyright Joyent, Inc. and other Node contributors. All rights reserved. </text>

The value of "LicenseConcluded" is in this example "LicenseRef-MIT". The SPDX2TV file contains also the following tags and values:

> **LicenseID:** LicenseRef-MIT
> 
> **LicenseName:** MIT License
> 
> **ExtractedText:** <text> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. </text>

As one can see, having the path and the name of the files used in the build it is very easy to extract the necessary license and copyright information from the SPDX2TV files. If file and path is cannot be used the given file hashes can be used alternatively.

## Glossary
The quality and, above all, the consistency of the curated material depend on a jointly held perspective and general understanding among the maintainer and contributors with respect to the legal and technical background of Open Source software licensing. In order to make their common approach transparent and provide a platform for further discussion, a working group of lawyers and software developers involved in the project has compiled a [glossary](/Glossary-English-version.md) of terms and concepts. Comments, additions, and changes are of course always welcome.

## Further Work
The following tasks are on the todo list:
* provide tools to ease the generation of compliance artifacts in the CI/CD pipelines
* additionally we provide other license compliance relevant artifacts, which might be of value for others.

In case you want to contribute to the above mentioned topics - everything is highly welcome
