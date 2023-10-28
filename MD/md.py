from command import mpirun_command
import os


class MDExecuter:

    def __init__(self, settings, tpr_file_name=None, input_dir=None, output_dir=None):
        self.tpr_file_name = tpr_file_name
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.settings = settings

    def single_md(self, total_process, threads_per_process):
        if self.settings.gpu:
            os.system(self.execute_gpu_command(total_process, threads_per_process))
        else:
            os.system(self.execute_cpu_command(total_process, threads_per_process))

    def execute_gpu_command(self, total_process, threads_per_process):
        command = (
            mpirun_command(total_process) +
            'mdrun' +
            ' -s ' + os.path.join(self.input_dir, 'topol.tpr') +
            ' -o ' + os.path.join(self.output_dir, 'traj.trr') +
            ' -x ' + os.path.join(self.output_dir, 'traj_comp.xtc') +
            ' -e ' + os.path.join(self.output_dir, 'ener.edr') +
            ' -g ' + os.path.join(self.output_dir, 'md.log') +
            ' -c ' + os.path.join(self.output_dir, 'confout.gro') +
            ' -cpo ' + os.path.join(self.output_dir, 'state.cpt') +
            ' -pme ' + 'gpu' +
            " -v -ntomp " + str(threads_per_process)
        )
        return command

    def execute_cpu_command(self, total_process, threads_per_process):
        command = (
            mpirun_command(total_process) +
            'mdrun' +
            ' -s ' + os.path.join(self.input_dir, 'topol.tpr') +
            ' -o ' + os.path.join(self.output_dir, 'traj.trr') +
            ' -x ' + os.path.join(self.output_dir, 'traj_comp.xtc') +
            ' -e ' + os.path.join(self.output_dir, 'ener.edr') +
            ' -g ' + os.path.join(self.output_dir, 'md.log') +
            ' -c ' + os.path.join(self.output_dir, 'confout.gro') +
            ' -cpo ' + os.path.join(self.output_dir, 'state.cpt') +
            " -v -ntomp " + str(threads_per_process)
        )
        return command

    def multi_md(self, parallel, multi_dir_pathes: list, total_process: int, threads_per_process: int):
        chunk_size = parallel
        splitted_pathes = [multi_dir_pathes[i:i+chunk_size] for i in range(0, len(multi_dir_pathes), chunk_size)]
        for pathes in splitted_pathes:
            multi_dir = ' '.join(pathes)
            if self.settings.gpu:
                if len(pathes) == parallel:
                    multi_dir = ' '.join(pathes)
                    os.system(self.execute_gpu_multi_command(multi_dir, total_process, threads_per_process))
                else:
                    multi_dir = ' '.join(pathes)
                    process = len(pathes)
                    os.system(self.execute_gpu_multi_command(multi_dir, process, threads_per_process))
            else:
                if len(pathes) == parallel:
                    multi_dir = ' '.join(pathes)
                    os.system(self.execute_cpu_multi_command(multi_dir, total_process, threads_per_process))
                else:
                    multi_dir = ' '.join(pathes)
                    process = len(pathes)
                    os.system(self.execute_cpu_multi_command(multi_dir, total_process, threads_per_process))

    def execute_gpu_multi_command(self, multi_dir_pathes, total_process, threads_per_process):
        command = (
            mpirun_command(total_process) +
            'mdrun' +
            ' -multidir ' + multi_dir_pathes +
            ' -s ' + 'topol' +
            ' -v ' +
            ' -pme ' + 'gpu' +
            ' -npme ' + '1' +
            ' -ntomp ' + str(threads_per_process)
        )
        return command

    def execute_cpu_multi_command(self, multi_dir_pathes, total_process, threads_per_process):
        command = (
            mpirun_command(total_process) +
            'mdrun' +
            ' -multidir ' + multi_dir_pathes +
            ' -s ' + 'topol' +
            ' -v ' +
            ' -ntomp ' + str(threads_per_process)
        )
        return command
