# package-analysis
This repo contains license and copyright analysis results of open source packages. It further contains other license compliance relevant artifacts, which might be of value for others.

The objective of the project is to lower the required effort for all who want to make use of OSS in a license compliant way. 

To achieve this we will develop, share and improve the artifacts commonly used to fulfill the requirements of the different Free and Open Source Software licenses by applying the Open Source Software development principles. This may turn Open Source license compliance into a straight forward task. 

Another objective is a very close collaboration with the OSS community in order to fix detected "bugs" in licensing as well as introducing the information needed for license compliance activities in the Open Source projects, i.e. provide our analysis work to the OSS projects.

One of the tasks in OSS compliance work is the analysis of OSS packages in order to identify the licenses and copyright holders. Although tools are available which support the analysis, it is still the task which causes effort.
We believe that is does not make any sense that everyone doing checks of packages again and again. This is redundant effort in our opinion which could be much better invested in OSS development. In other words: we think increasing the code base is much better instead of spending effort for license compliance checks which are done thousand fold today in many different organizations.

## Provided Artifacts

The analysis results are provided in the "analysed-packages" directory. Usually two artifacts are provided a SPDX tag-value file and a ready to use OSS-disclosure file. The main difference between both is that the tag-value files can be used and integrated in the build process in a way that only the licenses of those files are considered which will end up in the build artifact. Furthermore the tag-value files contain notes on license conclusions to make decisions transparent if necessary. The OSS-disclosure files contain all applicable licenses and all copyright notices of the entire package. Additionally to this the OSS-disclosure files contain "acknowledgment texts" if such an acknowledgment is required be the license.

## Process we follow in order to create a OSS package analysis file
We create such OSS package analysis files and make them available for download under the terms of the Creative Commons Public Domain Dedication [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/). We know that the content we produce is somehow delicate. Due to this it is important to disclose how we create such content. Since we represent an Open Source project everything is transparent. The following points describe the procedure we follow in creating the "OSS package analysis file" as we call it. 

The OSS package analysis file are generated following the process described below:

* Obtain the component in source code form
	* download the component from the official web site / check the hashes
	* the component is provided by a third party
	* the download URL is provided in the README files of the corresponding directories
* Issue a license and copyright analysis with the GPL-2.0 licensed tool FOSSology. FOSSology searches in files for the following information:
	* License relevant text phrases
	* Copyright strings
* A licensing expert person will review and analyze the FOSSology result. The expert person is not necessarily a lawyer, but has several years of experience in license compliance activities.
* For the analysis of the OSS packages we currently use [FOSSology](https://www.fossology.org/)

## Further Work
The following tasks are on the todo list:
* creating a nice website
* creating a project logo
* providing a REST API to search for and download the analysis results to enable for automation and integration in CI/CD pipelines

In case you want to contribute to the above mentioned topics - everything is highly welcome