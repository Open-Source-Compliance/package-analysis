import os


class FolderCleaner:
    def __init__(self, path: str):
        self.path = path
        self.clean_folder()
    
    def clean_folder(self):
        try:
            files = os.listdir(self.path)
            for file in files:
                file_path = os.path.join(self.path , file)
                if os.path.isfile(file_path):
                    if "placeholder" not in file:
                        os.remove(file_path)
            print(f"All files in {self.path} are deleted successfully.")
        except OSError:
            print("Error occurred while deleting files.")