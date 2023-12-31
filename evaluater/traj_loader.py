import mdtraj as md
import numpy as np

class TrajLoader:

    def __init__(self):
        self.trajectory = None
        self.topology = None

    def load(self, traj_file_path, gro_file_path):
        obj = md.load(traj_file_path, top=gro_file_path)
        self.trajectory = obj
        self.topology = obj.topology

    def select_atoms(self, from_index, to_index):
        return self.trajectory.atom_slice(self.topology.select('index {} to {}'.format(from_index, to_index)))

    def select_residue(self, target_residues):
        return self.trajectory.atom_slice(self.topology.select('resid ' + target_residues))

    def load_gro(self, gro_file_path, target_residue=None):
        if target_residue == None:
            self.trajectory = md.load(gro_file_path)
            self.topology = self.trajectory.top
        else:
            traj = md.load(gro_file_path)
            self.trajectory = traj.atom_slice(traj.top.select('resid {}'.format(target_residue)))
            self.topology = self.trajectory.top

    def select_C_alpha(self):
        return self.trajectory.atom_slice(self.topology.select('name CA'))

    def select_backbone(self):
        return self.trajectory.atom_slice(self.topology.select('backbone'))
