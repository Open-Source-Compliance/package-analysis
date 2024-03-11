### Installations
One prepare the setup for installation either via docker or via virtual environment.

## Via docker
You need to first install docker in order to proceed to next steps

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
    :\> .\demoEnv\Scripts\activate
    ```

4. Install the requirements

    ```sh
    >  pip install -r requirements.txt
    ```