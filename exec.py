import sys
import argparse
sys.path.append('./')
import logging
from executePaCSMD import PaCSMDExecuter
from setter import MDSetter

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    # コマンドライン引数を定義
    parser.add_argument('--gpu', type=int, help='ワーキングディレクトリ')
    parser.add_argument('--ngpus', type=int, help='nodeの数')
    parser.add_argument('--process_per_node', type=int, help='gpuの数',)
    parser.add_argument('--threads_per_process', type=int, help='総プロセス数')
    parser.add_argument('--node', type=int, help='リスタートするかどうか1 or 0',)
    parser.add_argument('--nbins', type=int, help='pacsmdの手法', default=50)
    parser.add_argument('--nround', type=int, help='スレッド数', default=100)
    parser.add_argument('--parallel', type=int, help='distPaCSMDなら指定', default=2)
    parser.add_argument('--how_many', type=int, help='distPaCSMDなら指定', default=1)
    parser.add_argument('--threshold', type=float, help='上限距離', default=0.1)
    parser.add_argument('--target', type=str, help='resid from id to id')
    parser.add_argument('--file_name', type=str, help='delaunay ファイル名', default='delaunay.pkl')
    parser.add_argument('--work_dir', type=str, help='パス', default='./')

    arg = parser.parse_args()
    arranged_args = { k: v for k, v in vars(arg).items() if v is not None }
    work_dir = arranged_args.pop('work_dir')
    settings = MDSetter(**arranged_args)
    PaCSMDExecuter(work_dir, settings).execute_Delaunay_PaCS_MD()
