import argparse, subprocess, datetime, os, pdb, sys
from Utils.CichlidActionRecognition import ML_model
from Utils.DataPrepare import DP_worker


parser = argparse.ArgumentParser(description='This script takes video clips and annotations, either train a model from scratch or finetune a model to work on the new animals not annotated')

parser.add_argument('--ML_videos_directory',
                    type = str, 
                    default = '/data/home/llong35/data/labeled_videos',
                    required = False, 
                    help = 'Name of directory to hold all video clips')
                    
parser.add_argument('--Clips_annotations',
                    type = str, 
                    default = '/data/home/llong35/patrick_code_test/test.csv',
                    help = 'project each animal belongs to')
                    
parser.add_argument('--Train_json',
                    type = str, 
                    default = '/data/home/llong35/temp/test_JAN_7_temp/source.json',
                    help = 'json file previously used for training')
                    
parser.add_argument('--Purpose',
                    type = str, 
                    default = 'classify',
                    help = 'classify is the only function for this script for now')


# Temp directories that wlil be deleted at the end of the analysis
parser.add_argument('--Clips_temp_directory',
                    default=os.path.join(os.getenv("HOME"),'clips_temp'),
                    type = str, 
                    required = False, 
                    help = 'Location for temp files to be stored')

# Parameters specific for finetuning for other animals
parser.add_argument('--resume_path',
                    default='/data/home/llong35/temp/test_JAN_7_temp/save_30.pth',
                    type=str,
                    help='Save data (.pth) of previous training')

# Output data
parser.add_argument('--Results_directory',
                    type = str,
                    default=os.path.join(os.getenv("HOME"),'temp','test_JAN_15_temp'),
                    help = 'directory to store sample prepare logs')

# Parameters for the dataloader
parser.add_argument('--sample_duration',
                    default=96,
                    type=int,
                    help='Temporal duration of inputs')
                    
parser.add_argument('--sample_size',
                    default=120,
                    type=int,
                    help='Height and width of inputs')
                    
parser.add_argument('--n_threads',
                    default=5,
                    type=int,
                    help='Number of threads for multi-thread loading')


# Parameters for the optimizer
parser.add_argument('--learning_rate',default=0.1,type=float,help='Initial learning rate (divided by 10 while training by lr scheduler)')
parser.add_argument('--momentum', default=0.9, type=float, help='Momentum')
parser.add_argument('--dampening', default=0.9, type=float, help='dampening of SGD')
parser.add_argument('--weight_decay', default=1e-5, type=float, help='Weight Decay')
parser.add_argument('--nesterov', action='store_true', help='Nesterov momentum')
parser.set_defaults(nesterov=False)
parser.add_argument('--optimizer',default='sgd',type=str,help='Currently only support SGD')
parser.add_argument('--lr_patience',default=10,type=int,help='Patience of LR scheduler. See documentation of ReduceLROnPlateau.')
parser.add_argument('--resnet_shortcut',default='B',help='Shortcut type of resnet (A | B)')


# Parameters for data augmentation
parser.add_argument('--no_hflip',action='store_true',help='If true holizontal flipping is not performed.')
parser.set_defaults(no_hflip=False)
parser.add_argument('--no_vflip',action='store_true',help='If true vertical flipping is not performed.')
parser.set_defaults(no_hflip=False)


# Parameters for general training
parser.add_argument('--checkpoint',default=10,type=int,help='Trained model is saved at every this epochs.')


# Parameters specific for training from scratch
parser.add_argument('--n_classes',default=10,type=int)
parser.add_argument('--batch_size', default=13, type=int, help='Batch Size')
parser.add_argument('--n_epochs',default=200,type=int,help='Number of total epochs to run')




args = parser.parse_args()


def check_args(args):
    if not os.path.exists(args.Results_directory):
        os.makedirs(args.Results_directory)
    if not os.path.exists(args.Clips_temp_directory):
        os.makedirs(args.Clips_temp_directory)

os.environ["CUDA_VISIBLE_DEVICES"]="0"
check_args(args)
data_worker = DP_worker(args)
data_worker.work()
ML_model = ML_model(args)
ML_model.work()