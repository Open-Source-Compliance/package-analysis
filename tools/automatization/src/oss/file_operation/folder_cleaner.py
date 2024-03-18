from pathlib import Path


class FolderCleaner:
    def __init__(self, path: str):
        self.path = path
        self.clean_folder()

    def rmdir(self, directory):
        directory = Path(directory)
        for item in directory.iterdir():
            if "placeholder" in str(item):
                continue
            if item.is_dir():
                self.rmdir(item)
            else:
                item.unlink()
        if "output" not in str(directory):
            directory.rmdir()

    def clean_folder(self):
        try:
            print("---------------------------------------------------------------------------\n")
            self.rmdir(self.path)
            print(f"All files in {self.path} are deleted successfully.\n")
        except OSError as e:
            print(f"Error occurred while deleting files. Error is {e}")