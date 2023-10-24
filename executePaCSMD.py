from manipulate_file import FileLoader
from PaCS_MD import PaCSMD
import os, shutil, glob
class PaCSMDExecuter:

    def __init__(self, base_dir, settings):
        self.base_dir = base_dir
        self.settings = settings

    def execute_Delaunay_PaCS_MD(self):
        for i in range(1, self.settings.how_many+1, 1):
            dir_path = os.path.join(self.base_dir, 'trial{}'.format(i))
            self.make_dir(dir_path)
            for pattern in self.settings.patterns:
                self.copy_files(pattern, self.base_dir, dir_path)
            PaCSMD(dir_path, self.settings).execute_delaunay_pacs_md(delaunay_data=self.load_delaunay_data(self.settings.file_name))

    def make_dir(self, dir, exist=True):
        os.makedirs(dir, exist_ok=exist)

    def copy_files(self, pattern, dir1, dir2):
        for file_path in glob.glob(os.path.join(dir1, pattern)):
            shutil.copyfile(file_path, os.path.join(dir2, os.path.basename(file_path)))

    def load_delaunay_data(self, file_name):
        path = os.path.join(self.base_dir, file_name)
        return path


