from evaluater import BaseEvaluater, TrajLoader
import numpy as np
import types


class DelaunayEvaluater(BaseEvaluater):

    def __init__(self, sorted_delaunay_data, threshold=0.1):
        '''
        delaunay_data = [(index, np.array([x, y, z]))]
        '''

        super().__init__()
        self.sorted_delaunay_data = sorted_delaunay_data
        self.target_point = None
        self.target = None
        self.count = 0
        self.num_of_data = len(self.sorted_delaunay_data)
        self.threshold = threshold
        self.is_finished = False

    def set_target(self):
        print(self.sorted_delaunay_data)
        self.target, self.target_point = self.sorted_delaunay_data[self.count]

    def evaluate(self):
        if self._is_close_enough():
            if not self.is_target_remained():
                self.is_finished = True
            else:
                self.count += 1
                self.set_target()
        else:
            pass

    def _is_close_enough(self):
        if self.distance(self.sorted_list[0][1], self.target_point) <= self.threshold:
            return True
        else:
            return False

    def is_target_remained(self):
        return self.count < self.num_of_data

    def find_close_traj(self, traj_dict, tops=30) -> list:
        self.sorted_dict, self.sorted_list = self.sort_dict(traj_dict, lambda x: self.distance(x[1], self.target_point))
        self.traj_list = []
        for i in range(tops):
            self.traj_list.append(self.sorted_list[i][0])
        return self.traj_list
