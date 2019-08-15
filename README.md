# SGE Experiment Runner
Tool to generate SGE scripts based on an experiment config. The program expects a yaml file `config/experiments.yaml` and a script to run `config/base.sh` (both have been pre-populated with an example).

## Installation
```
$ git clone git@github.com:jackdeadman/sge-experiment-runner.git
$ pip install -r requirements.txt
```

## Experiments.yaml
The highest level keys represent the different experiement setups. The special key "base" is not an experiment, all experiments inherit attributes from base (these can be overidden). Each key value pair inside an experiment is passed to `config/base.sh` in the form `--key value --key2 another_value etc.`

## Running an experiment
```
python run_experiment.py experiment_name [queue]
```
The queue parameter is optional and if not specified the base queue config will be used. See the example config to see how to add additional queues.

Using the example config:

```
python run_experiment.py mse rse
```

The resulting "sge" file will be displayed and you will be prompted to whether you want to submit this job. This will create the file and place it inside the `sge_scripts` directory and resulting log files from the job will be dumped to `logs`

Generated SGE file:

```
#$ -M jdeadman1@sheffield.ac.uk
#$ -m bea
#$ -l rmem=16G,gpu=1,h_rt=24:00:00
#$ -o logs/mse/20190814-154641.log
#$ -j y
#$ -q rse.q
#$ -P rse
source ~/.bashrc
module load libs/cudnn/7.5.0.56/binary-cuda-9.0.176
loadconda
conda activate video-features

python example.py --learning_rate 0.0001 --batch 100 --images video_frames_small.flist --epochs 5 --loss mse --name mse
```
