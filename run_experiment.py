import sys
import yaml
import os
import time

CONF = 'config/experiments.yaml'
PROGRAM = 'config/base.sh'
SCRIPT_DUMP = 'sge_scripts'

def experiment_and_queue():
    experiment = sys.argv[1]
    queue = 'base'

    # Optionally specify a different queue
    if len(sys.argv) > 2:
        queue = sys.argv[2]
    
    return experiment, queue

def build_options(name, yaml_file):
    return { **yaml_file['base'], **yaml_file[name] }

def create_sge_flags(options, experiment):
    flags = ''
    for key, value in options.items():
        flags += '#$ -%s %s\n' % (key, value)
    date = time.strftime("%Y%m%d-%H%M%S")

    # Bind values for the variables "name" and "date"
    flags = flags.replace('{:name}', experiment).replace('{:date}', date)
    return flags

def create_command(options):
    flags = ' '.join([ '--%s %s' % (flag, value) for flag, value in options.items() ])
    return flags

def interactive_select(experiments):
    # Only import if we need to use it
    from PyInquirer import prompt
    # Currently only display ones in the base experiment
    queues = list(experiments.values())[0]['sge'].keys()
    questions = [
        {   'type': 'list',
            'name': 'experiment',
            'message': 'Select the experiment to run',
            'choices': experiments.keys()
        },

        {   'type': 'list',
            'name': 'queue',
            'message': 'Select the queue to use',
            'choices': queues
        }
    ]

    res = prompt(questions)
    experiment, queue = res['experiment'], res['queue']
    return experiment, queue

def main():

    with open(CONF) as f:
        experiments = yaml.load(f)

    if len(sys.argv) == 1:
        experiment, queue = interactive_select(experiments)
    else:
        experiment, queue = experiment_and_queue()

    options = build_options(experiment, experiments)
    options['name'] = experiment
    queue_config = build_options(queue, options['sge'])
    del options['sge']

    filecontents = create_sge_flags(queue_config, experiment)
    with open(PROGRAM) as f:
        filecontents += f.read().replace("\"$@\"", create_command(options))
    
    # Display the file we are about to create
    print(filecontents)

    if input('===== \nSubmit this? (y/N): ').lower() == 'y':
        os.system('mkdir -p logs/' + experiment)
        filename = os.path.join(SCRIPT_DUMP, experiment + '.' + queue +  '.sge')
        with open(filename, 'w') as f:
            print(filecontents, file=f)
        
        # Submit the job
        os.system('qsub ' + filename)

if __name__ == "__main__":
    main()