# Installations and Running Scripts

One can prepare the setup either via docker or via virtual environment.

# Preparation before running script

Whether you use docker or virtual env, you need to first prepare some steps

1. Move ReadmeXXXXX.txt and SPDX2TVXXXXX.spdx to input folder

2. Replace your name instead of XXXXX in "Person: XXXXX" in  config.yaml

Note:

```
In case there is a hash in the name of txt and spdx file, please do the following steps:

    1. Make input folder empty and then copy the two files there.

    2. Write the name of package inside config.yaml

```

## Via docker

### Installation

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

## Via virtual environment

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

    ```sh
    > cd src
    > python -m oss -c config.yaml
    ```
    Note:
    
    one can only once write his/her name in config file and change package_name (via -pn) everytime you run the scripts. See example below

    ```
    > python -m oss -c config.yaml -pn jQuery-MD5-2011.06.13

    ```