## How about liability?
One of the main questions or concerns which might hinder either the use or the contribution of OSS package analysis files is the question whether we or the contributor will be liable if there is a mistake in such a file. 
In order to answer this fundamental question we asked for legal advice. The following is the summary of the legal advice in our words:
Assuming that those files are protected by copyright they need to be licensed so that they can be used. We license the files under CC0 1.0 which is very near to "public domain" to make the use to them as easy as possible. Furthermore, the files can be downloaded and used ‘free of charge’.
These documents are so to say a donation. For donations there is liability only in case of willfulness or in a case of gross negligence. The process how the files are generated and which tools are used is described. Therefore, it can be reviewed and the tools can be evaluated. Moreover, the persons who process the tool output do have several years of experience in this area. We think that the risk of being liable is very little.
As any other OSS project, we also have implemented the common approach how to improve and to ensure quality. If you have doubts about the correctness of the content of the  OSS package analysis files you simply can file an issue and we will look at it, analyze it, provide feedback and in case there is an error in such a file we will correct it in a timely manner.

## Can I rely on the content of the license analysis files?
This question depends on your point of view, whether you trust this project and whether you think that the way how the files are generated is suited to provide accurate and reliable information.
We think that the process is defined in a way that following it will result in high quality information; nevertheless there is always the possibility that a used tool misses information or the person who processes the tool output makes a mistake. If you identify an error we are happy if you file an issue so that we are able to fix it.

You are able to evaluate, review and compare the published results with your own results, if you identify differences you can re-check your results or file an issue here. Even if you do not trust in the here published result, this project helps you to do a cross check of the quality of your implemented processes.

## Which process do we follow in order to create an OSS package analysis file?
We create such OSS package analysis files and make them available for download under the terms of the Creative Commons Public Domain Dedication [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/). We know that the content we produce is somehow delicate. Due to this it is important to disclose how we create such content. Since we represent an Open Source project everything is transparent. The following points describe the procedure we follow in creating the "OSS package analysis file" as we call it. 

The OSS package analysis file are generated following the process described below:

* Obtain the component in source code form:
	* download the component from the official web site / check the hashes
	* the source code of the component is provided by a third party (in case the source code package is provided by a third party, it will be mentioned explicitly
* Issue a license and copyright analysis with the GPL-2.0 licensed tool FOSSology. FOSSology searches in files for the following information:
	* License relevant text phrases
	* Copyright strings
	* Keywords for ECC (Export, Control and Customs)
* An OSS compliance expert will review and analyze the FOSSology result. The expert person, but has several years of experience in license compliance activities. Once this is done the OSS package analysis file will be available in the for-review directory, after having received a review it will be moved to the reviewed directory.
* Result is reviewed by a person who has more experience in license compliance activities than the author.
* The final result is made available in form of a Debian copyright file or a SPDX document or another "machine & human friendly" format.
* For the analysis of the OSS packages we currently use [FOSSology](http://www.fossology.org/projects/fossology)

## What quality assurance process do we follow when we receive OSS package analysis files as a contribution?

Here we distinguish two cases:
### Initial contribution
This means a complete package analysis file is contributed of a package which is not contained here already.
* We inspect the package with FOSSology and do a plausibility check of the content of the document based on the FOSSology information. So we will do a review (see below)
* We will make the information available what we compared during the plausibility check

### Update / bug fix 
In this case we will verify the bug fix; i.e. check the information of the file of the package whether the bug report / fix is correct

## Review of an OSS package analysis file

To do a good review is similar to the license analysis itself. The following tips shall provide good practices of how to do a "good" review. It is not meant to be complete and will be enhanced, whenever we see new topics to be covered.

### What is needed to do a "good" review:
1. the component source code
2. a license analysis tool, were you can review the license decisions like FOSSology. A simple license scanner without review capabilities  won't do the job.
3. the OSS package analysis file to be reviewed
4. a certain level of know how

### Topics to be checked / verified during the review

The following list provides topics a reviewer shall check:
1. is a main license assigned?
2. are all copyright strings "cleaned", i.e. contain no garbage ( e.g. *, //, dnl,...) ?
3. is there ECC relevant information and is this represented somewhere?
4. do the license texts contain garbage, like comment characters ( e.g. *, //, dnl,...)?
5. do the license texts contain the "correct license text"? E.g. is this the real, potentially customized BSD license?
6. is every from the scanner identified license concluded by a reviewer?
7. do the analysis file contain strange or unknown license names as concluded licenses? E.g. license "names" like Apache-possibility, zlib-possibiliy, GPL without version number, Apache without  version number, LGPL without version number, BSD, unclassified license, see file, see doc other, etc. shall no appear as concluded license
8. are the licenses classified correctly? if you are using risk levels check whether all concluded licenses are correct classified
9. if there are acknowledgments required by one or more licenses, are the relevant acknowledgments with all required elements contained in the OSS package analysis file?

	For example the CC licenses have other requirements concerning the content of the acknowledgment than Apache-2.0
11. in case you are working with the license obligation feature of FOSSology are all obligations of all concluded licenses covered?
12. are un-obvious license conclusions explained that others can reiterate the decision? This is especially important for license references which are internet links?

## What is the naming convention of the content in the OSS package analysis files directory?
The naming convention is straight forward, it is like this:

OSS-Package-Analysis-Files
	|
	|
	package-name
		|
		|
		--- version
		
