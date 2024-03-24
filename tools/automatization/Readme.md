# Installations and Running Scripts

One can prepare the setup either via docker or via virtual environment.

## Preparation before running script

Whether you use docker or virtual env, you need to first prepare some steps

1. **Input folder**: 

    Move ReadmeXXXXX.txt and SPDX2TVXXXXX.spdx to **input** folder (src/document-generations/**input**). Please clean inpit folder before moving the files

    ```
        ├── Dockerfile
        ├── Readme.md
        └── src
            ├── config.yaml
            ├── document-generations
            │   ├── input
            │   └── output
            ├── oss
            ├── README.md
            ├── requirements.txt
            └── setup.py
    ```

2. **Creator_name**:

    Replace your name instead of XXXXX in "creator_name : XXXX" in  

    1. config.yaml
        ```
        creator_name : XXXXX
        ```
    2. command line with -cn configuration flag
        ```
        python -m oss -cn XXXXX
        ```

3. **Package_name** and **package_version**:

    If the name of package has packagename and package version. It will automaitcally parses the name of the file and finds the package name and package version.

    **Note**:  In some cases, it can not parse the name of the file correctly. You can use either config.yaml or command line in those cases

    1. config.yaml
        ```
        package_name : update-rc.d
        package_version : 0.8
        ```
    2. command line with -pn and -pv configuration flag
        ```
        python -m oss -pn update-rc.d -pn package_name -pv package_version
        ```
4. **Remove_output**:

    You can optionally remove the output folder before generation of files. One can achieve this by updating config.yaml or command line

    1. config.yaml
        ```
        remove_output : true
        ```
    2. command line with -pn and -pv configuration flag
        ```
        python -m oss -rmo true
        ```
5. **Download_link**:

    This link will be saved inside Readme file.You can use either config.yaml or command line to set this value

    1. config.yaml
        ```
        download_link : https://git.yoctoproject.org/update-rc.d/snapshot/update-rc.d-0.8.tar.gz
        ```
    2. command line with -dl configuration flag
        ```
        python -m oss -dl https://git.yoctoproject.org/update-rc.d/snapshot/update-rc.d-0.8.tar.gz
        ```
5. **Reviewer**:

    You can add the name of the reviewer to the Readme.You can use either config.yaml or command line to set this value

    1. config.yaml
        ```
        reviewer : YYYYY
        ```
    2. command line with -dl configuration flag
        ```
        python -m oss -r YYYYY
        ```

### Via docker

You need to first install docker in order to proceed to next steps

1. Install docker for your OS

2. Build the image with docker

    ```
    >$  docker build . -t automatization_app
    ```

3. Mount your folder into docker. Give your absolute path to the itxpt_mqtt_example_nodejs folder
    ~~~
    >$ docker run -it -v /home/parian/work/fossology/pago-package-analysis/tools/automatization/src/:/app/ automatization_app
    ~~~
4. After execution, try to change the permission of the files in output folder
    ~~~
    >$ cd src/oss/output/ && sudo chmod 777 *
    ~~~

### Via virtual environment

You need to first install python, git, pip in order to proceed to next steps

1. Install virtual environment

    Linux
    ```
    >$ python3 -m pip install --user virtualenv
    ```

    Windows
    ```
    :\> py -m pip install --user virtualenv
    ```

2. Create virtual environment inside python folder

    Linux
    ```
    >$ python3 -m venv demoEnv
    ```

    Windows
    ```
    :\> py -m venv demoEnv
    ```

3. Source the virtual environment

    Linux
    ```
    >$ . demoEnv/bin/activate
    ```

    Windows
    ```
    :\> ./demoEnv/Scripts/activate

    ```

4. Install the requirements

    ```sh
    >  cd  src  && pip install -r requirements.txt
    ```

5. Run the sripts

    One can set all the necessary configuration parameters inside config.yaml or running them via command line. You can find  the available configuration parameters by running this command

    ```sh
    > cd src
    > python -m oss --help
    ```

    5.1 Config.yaml

    ```sh
    > cd src
    > python -m oss -c config.yaml
    ```

    5.2 Command line 
    
    As you can see below, I can give some of the parameters via command line (e.g. package_name and Package_version)

    ```sh
    > cd src
    > python -m oss -c config.yaml -pn jQuery-MD5 -pv 2011.06.13

    ```
## Generated Output

Whether you use docker or virtual environment, you should have the generated documents inside **output** folder.

```
.
└── package_name
    └── package_version
        ├── README.md
        ├── package_name-package_version-OSS-disclosure.txt
        ├── package_name-package_version-SPDX2TV.spdx
        ├── package_name-package_version.spdx.json
        ├── package_name-package_version.spdx.rdf.xml
        └── package_name-package_version.spdx.yaml

```
As an example, the output folder for update-rc.d will look like this.

```
.
└── update-rc.d
    └── version-0.8
        ├── README.md
        ├── update-rc.d-0.8-OSS-disclosure.txt
        ├── update-rc.d-0.8-SPDX2TV.spdx
        ├── update-rc.d-0.8.spdx.json
        ├── update-rc.d-0.8.spdx.rdf.xml
        └── update-rc.d-0.8.spdx.yaml

```