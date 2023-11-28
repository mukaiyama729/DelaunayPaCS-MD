import mdtraj as md
from evaluater import TrajLoader
import numpy as np
import logging
logger = logging.getLogger('pacs_md')

class TrajManipulater:

    def __init__(self, traj_objs: dict):
        '''
        traj_objs = { (1, 2): Trajectory, ... }
        '''
        self.traj_objs: dict = traj_objs

    def all_trajectories_com(self):
        all_trajes = {}
        for cyc_rep, trj_obj in self.traj_objs.items():
            merged_trj = np.concatenate((trj_obj.time.reshape(-1,1), self.traj_com(trj_obj)), axis=1)
            for i in range(len(merged_trj)):
                key = (cyc_rep[0], cyc_rep[1], merged_trj[i,0])
                value = merged_trj[i,1:]
                all_trajes[key] = value
        logger.info('all trajectory com: {}'.format(all_trajes))
        return all_trajes

    def traj_com(self, traj_obj: md.Trajectory):
        return md.compute_center_of_mass(traj_obj)

    def traj_mean(self, traj_obj: md.Trajectory):
        meaned_xyz = traj_obj.xyz.mean(axis=1).astype(np.float64)
        return meaned_xyz

    def all_trajectories_mean(self):
        all_trajes = {}
        for cyc_rep, trj_obj in self.traj_objs.items():
            merged_trj = np.concatenate((trj_obj.time.reshape(-1,1), self.traj_mean(trj_obj)), axis=1)
            for i in range(len(merged_trj)):
                key = (cyc_rep[0], cyc_rep[1], merged_trj[i,0])
                value = merged_trj[i,1:]
                all_trajes[key] = value
        logger.info('all trajectory com: {}'.format(all_trajes))
        return all_trajes
