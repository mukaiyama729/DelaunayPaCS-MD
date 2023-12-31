class MDSetter:

    file_to_pattern = { 'topol': 'topol*.top', 'index': 'index*.ndx', 'input': 'input*.gro', 'md': 'md*.mdp', 'posres': '*.itp', 'sel': 'sel.dat' }
    patterns = ['*.top', '*.itp', '*.gro', '*.dat', '*.ndx', '*.mdp']

    @classmethod
    def set_MD(cls, gpu: bool, ngpus: int, process_per_node, threads_per_process, node):
        cls.gpu = gpu
        cls.ngpus = ngpus
        cls.process_per_node = process_per_node
        cls.threads_per_process = threads_per_process
        cls.node = node
        cls.total_processes = cls.process_per_node * cls.node

    @classmethod
    def set_delaunay_MD(cls, nbins, nround, parallel, target, how_many=1, file_name='delaunay_data', threshold=0.1):
        cls.nround = nround
        cls.parallel = parallel
        cls.how_many = how_many
        cls.nbins = nbins
        cls.target = target
        cls.file_name = file_name
        cls.threshold = threshold

    def __init__(self, gpu, ngpus, process_per_node=1, threads_per_process=1, node=1, nround=100, parallel=1, how_many=1, nbins=30, target='', align_target='', align_res='backbone', file_name='', threshold=0.1, dist_method='com', work_dir='./', gpu_ids='', gputasks='', npme='', pme='', nb='', pmefft='', bonded=''):
        self.gpu = gpu
        self.ngpus = ngpus
        self.process_per_node = process_per_node
        self.threads_per_process = threads_per_process
        self.node = node
        self.nround = nround
        self.parallel = parallel
        self.how_many = how_many
        self.nbins = nbins
        self.target = target
        self.align_target = align_target
        self.align_res = align_res
        self.file_name = file_name
        self.threshold = threshold
        self.dist_method = dist_method
        self.work_dir = work_dir
        self.total_processes = self.process_per_node * self.node
        self.gpu_ids = gpu_ids
        self.gputasks = gputasks
        self.npme = npme
        self.pme = pme
        self.nb = nb
        self.pmefft = pmefft
        self.bonded = bonded
        self.gpu_options = self.gpu_options()

    def gpu_options(self):
        options = ' '
        if self.gpu_ids:
            options += '-gpu_id ' + str(self.gpu_ids)
        if self.gputasks:
            options += '-gputasks ' + str(self.gputasks)
        if self.npme:
            options += '-nmpe ' + str(self.npme)
        if self.pme:
            options += '-pme ' + str(self.pme)
        if self.nb:
            options += '-nb ' + str(self.nb)
        if self.pmefft:
            options += '-pmefft ' + str(self.pmefft)
        if self.bonded:
            options += '-bonded ' + str(self.bonded)

        return options

