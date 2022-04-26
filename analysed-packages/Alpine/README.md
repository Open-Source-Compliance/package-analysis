## Structure and Content of the Directory
The structure of the directory is quite straightforward. There is one directory per Alpine version package, this directory contains the different directories of the analyzed packages.


## Analyzed Source Code
This is a description for non technical persons. 
The analyzed source code can be determined as follows: 
* Go to the git space of the component in the Alpine git. It contains the build files for the specific package, along with the required patches and scripts, etc.. 
* Download the content of the git space of the specific components
* Check the APKBUILD files to determine the fetched other components
* Download the source code of the fetched components. 

To provide full transparency for non technical persons, the links to the alpine git space as well as the links to the fetched other components during the execution of the APKBUILD file are provided in the Readme files of the different component directories.

