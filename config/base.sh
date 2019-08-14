source ~/.bashrc
module load libs/cudnn/7.5.0.56/binary-cuda-9.0.176
loadconda
conda activate video-features

python example.py "$@"
