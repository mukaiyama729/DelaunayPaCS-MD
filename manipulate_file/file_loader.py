import os
import numpy as np
import pickle

class FileLoader:

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def load_npy_file(self, file_name):
        return np.load(os.path.join(self.dir_path, file_name), allow_pickle=True)

    def load_pickle_file(self, file_name):
        with open(os.path.join(self.dir_path, file_name), 'rb') as f:
            delaunay_data = pickle.load(f)
        f.close()
        return delaunay_data
