from evaluater import BaseEvaluater, TrajLoader
from manipulate_data import Calculater
import numpy as np
import types
import logging
logger = logging.getLogger('pacs_md')

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

    def set_target(self, rot_trans=None):
        logger.info(self.sorted_delaunay_data)
        if rot_trans is None:
            self.target, self.target_point = self.sorted_delaunay_data[self.count]
        else:
            self.target, self.target_point = self.sorted_delaunay_data[self.count]
            logger.info('executing alignment')
            logger.info('rotation : {}'.format(rot_trans[0]))
            logger.info('translation : {}'.format(rot_trans[1]))
            self.target_point = Calculater().alignment(self.target_point, rot_trans[0], rot_trans[1]).flatten()
        logger.info('target is: {}'.format(self.target))
        logger.info('target point is: {}'.format(self.target_point))

    def evaluate(self):
        if self._is_close_enough():
            logger.info('close enough: {}'.format(self.target_point))
            if not self.is_target_remained():
                self.is_finished = True
                logger.info('is finished?: {}'.format(self.is_finished))
            else:
                logger.info('change target')
                self.count += 1
                target, target_point = self.sorted_delaunay_data[self.count]
                logger.info('next target is {}, next target point is {}'.format(target, target_point))
                logger.info('count: {}'.format(self.count))
                logger.info('is finished?: {}'.format(self.is_finished))
        else:
            logger.info('not close enough: {}'.format(self.target_point))
            pass

    def _is_close_enough(self):
        distance = self.distance(self.sorted_list[0][1], self.target_point)
        logger.info('distance: {}'.format(distance))
        if distance <= self.threshold:
            return True
        else:
            return False

    def is_target_remained(self):
        return self.count + 1 < self.num_of_data

    def find_close_traj(self, traj_dict, tops=30) -> list:
        self.sorted_dict, self.sorted_list = self.sort_dict(traj_dict, lambda x: self.distance(x[1], self.target_point))
        logger.info('sorted trajectory dict: {}'.format(self.sorted_dict))
        logger.info('sorted trajectory list: {}'.format(self.sorted_list))
        self.traj_list = []
        for i in range(tops):
            self.traj_list.append(self.sorted_list[i][0])
        return self.traj_list
