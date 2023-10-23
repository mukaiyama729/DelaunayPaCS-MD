import glob, os
from manipulate_file import FileLoader
from methods import DelaunayPaCSMD
from executePaCSMD import MDSetter

class FileError(Exception):
    pass

class PaCSMD:

    def __init__(self, work_dir):
        self.work_dir = work_dir

    def check_necessary_files(self) -> None:
        self.file_pathes = {}
        self.files = {}
        for file_name, pattern in MDSetter.file_to_pattern.items():
            self.check_file(file_name, pattern)

    def check_file(self, file_name: str, pattern) -> None:
        files = glob.glob(os.path.join(self.work_dir, pattern))
        if file_name == 'posres':
            self.file_pathes[file_name] = files
            self.files[file_name] = []
            if not(files):
                pass
            else:
                for file_path in files:
                    self.files[file_name].append(os.path.basename(file_path))
        else:
            if any(files) and len(files) == 1:
                self.file_pathes[file_name] = files[0]
                self.files[file_name] = os.path.basename(files[0])
            elif any(files) and len(files) > 1:
                self.file_pathes = files[0]
                self.files = os.path.basename(files[0])
            else:
                raise FileError

    def execute_delaunay_pacs_md(self, delaunay_data):
        DelaunayPaCSMD(
            delaunay_data,
            self.file_pathes,
            self.files,
            self.work_dir,
        ).execute()
