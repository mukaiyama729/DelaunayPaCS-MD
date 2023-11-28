import numpy as np
import mdtraj as md
import types


class BaseEvaluater:

    def __init__(self):
        self.traj_obj = None
        self.top_obj = None

    def load_obj(self, traj_obj):
        self.traj_obj = traj_obj
        self.top_obj = traj_obj.topology

    def distance(self, from_point, to_point):
        return np.linalg.norm(to_point - from_point)

    def com(self, from_time, to_time):
        return md.compute_center_of_mass(self.traj_obj[from_time, to_time+1])

    def sort_dict(self, _dict: dict, func: types.FunctionType):
        sorted_data = sorted(_dict.items(), key=func)
        sorted_dict = {key: value for key, value in sorted_data}
        return sorted_dict, sorted_data

