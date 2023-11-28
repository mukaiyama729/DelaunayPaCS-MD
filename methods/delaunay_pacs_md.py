from MD import MDExecuter
from manipulate_file import FileCreater
from evaluater import DelaunayEvaluater, TrajLoader
from manipulate_data import TrajManipulater, Calculater
import numpy as np
import os
import re
import logging
logger = logging.getLogger('pacs_md')

class DelaunayPaCSMD:

    def __init__(self, delaunay_data, initial_file_pathes, files, work_dir, settings):
        self.delaunay_data = delaunay_data
        self.initial_file_pathes = initial_file_pathes
        self.files = files
        self.work_dir = work_dir
        self.ranked_traj_list = []
        self.settings = settings

    def make_traj_data(self, dir_pathes):
        trj_data = {}
        pattern = r'-(\d+)-(\d+)'
        for dir_path in dir_pathes:
            match = re.search(pattern, dir_path)
            if match:
                cyc = int(match.group(1))
                rep = int(match.group(2))
                traj_file_path = os.path.join(dir_path, 'traj_comp.xtc')
                gro_file_path = self.initial_file_pathes['input']
                loader = TrajLoader()
                loader.load(traj_file_path, gro_file_path)
                target_trj_obj = loader.select_residue(self.settings.target)
                trj_data[(cyc, rep)] = target_trj_obj
        logger.info('maked traj data:{}'.format(trj_data))
        return trj_data

    def initial_md(self):
        logger.info('start initial MD')
        self.pacs_dir_pathes = []
        tpr_file_name = 'topol.tpr'
        creater = FileCreater(to_dir=self.work_dir)
        self.pacs_dir_pathes.append(creater.create_dir('pacs-0-0'))
        creater.change_to_dir(os.path.join(self.work_dir, 'pacs-0-0'))
        creater.copy_file(self.files['input'])
        creater.create_tpr_file(tpr_file_name, self.files, self.initial_file_pathes)

        MDExecuter(
            self.settings,
            tpr_file_name,
            input_dir=self.pacs_dir_pathes[0],
            output_dir=self.pacs_dir_pathes[0]
        ).single_md(1, self.settings.threads_per_process)

    def create_delaunay_evaluater(self, threshold):
        self.evaluater = DelaunayEvaluater(self.delaunay_data, threshold)
        self.evaluater.set_target()

    def execute(self):
        self.create_delaunay_evaluater(self.settings.threshold)
        self.initial_md()
        self.update_ranked_traj_list()

        self.round = 1

        while self.round <= self.settings.nround:
            self.prepare_for_md()
            self.parallel_md()
            is_finished = self.evaluate_result()
            if is_finished:
                break
            else:
                self.align_target()
                self.round += 1

    def prepare_for_md(self):
        self.pacs_dir_pathes = FileCreater(self.work_dir).create_dirs_for_pacs('pacs-{}'.format(self.round), self.settings.nbins)
        logger.info(self.pacs_dir_pathes)
        chosen_dict = {}
        for index, pacs_path in enumerate(self.pacs_dir_pathes):
            cyc, rep, time = self.ranked_traj_list[index]
            chosen_dict[index] = {'next_path': pacs_path, 'cyc': cyc, 'rep': rep, 'time': time}
            creater = FileCreater(pacs_path, from_dir=self.cyc_rep_path(cyc, rep))
            creater.create_input_file(self.files, time)
            creater.create_tpr_file('topol.tpr', self.files, self.initial_file_pathes)
        logger.info('chosen {}: {}'.format(self.round, chosen_dict))

    def cyc_rep_path(self, cyc, rep):
        return os.path.join(self.work_dir, 'pacs-{}-{}'.format(cyc, rep))

    def parallel_md(self):
        MDExecuter(self.settings).multi_md(
            parallel=self.settings.parallel,
            multi_dir_pathes=self.pacs_dir_pathes,
            total_process=self.settings.total_processes,
            threads_per_process=self.settings.threads_per_process,
            )

    def evaluate_result(self):
        self.update_ranked_traj_list()
        self.evaluater.evaluate()
        return self.evaluater.is_finished

    def update_ranked_traj_list(self):
        trj_data = self.make_traj_data(self.pacs_dir_pathes)
        if self.settings.dist_method == 'com':
            traj_dict = TrajManipulater(trj_data).all_trajectories_com()
            logger.info('distance method: com')
        elif self.settings.dist_method == 'mean':
            traj_dict = TrajManipulater(trj_data).all_trajectories_mean()
            logger.info('distance method: mean')
        else:
            traj_dict = TrajManipulater(trj_data).all_trajectories_com()

        self.ranked_traj_list = self.evaluater.find_close_traj(
            traj_dict,
            tops=self.settings.nbins
        )

    def align_target(self):
        base = TrajLoader()
        base.load_gro(os.path.join(self.pacs_dir_pathes[0], 'confout.gro'), self.settings.align_target)
        target = TrajLoader()
        target.load_gro(self.initial_file_pathes['input'], self.settings.align_target)
        transformed_target, rot_trans = Calculater().superimpose_coordinates(coord1=np.squeeze(base.trajectory.xyz), coord2=np.squeeze(target.trajectory.xyz))
        self.evaluater.set_target(rot_trans=rot_trans)
