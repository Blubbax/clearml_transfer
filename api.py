from clearml.backend_api.session.client import APIClient
from clearml.backend_api.session.client import StrictSession
from utils import transfer_model, transfer_task
from clearml import TaskTypes
import sys
import getopt

# Args

api_conf_source = ''
api_conf_target = ''

try:
    args, vals = getopt.getopt(
        sys.argv[1:],
        "hmo:",
        ['source', 'target']
    )

    for arg, val in args:
        if arg in ('-s', '--source'):
            api_conf_source = val
        elif arg in ('-t', '--target'):
            api_conf_target = val
            
except getopt.error as error:
    print(error)
    exit

if len(sys.argv) < 2:
    print("ERROR: not enough arguments passed")
    exit

task_ids = [
    '7f2a7105fcc743cb8f3f225f324e51bd',
    'c5e89d9085ec4ec68f13c8430d25ce19',
    'cf5a7e75f6754629a356f07704b7d106'
]

model_ids = [
    '731a44f3d5ce4a799cd67238bcea8b04'
]

target_project_name = "Transfer Testrr"

# Constants and Variables
transfer_tag_name = "LNU TRANSFER"
task_map = dict()
model_map = dict()

# Setup connections

session_source = StrictSession(config_file=api_conf_source)
session_target = StrictSession(config_file=api_conf_target)

source = APIClient(session=session_source)
target = APIClient(session=session_target)


# Check if target project exists

project_list = target.projects.get_all(name=target_project_name)
if len(project_list) > 0:
    target_project_id = project_list[0].id
else:
    print(f'INFO: Project {target_project_name} is not available on target instance. Project will be created')
    project = target.projects.create(name=target_project_name, tags=[transfer_tag_name])
    print('INFO: Project created')
    target_project_id = project.id


# Copy tasks
for task_id in task_ids:
    transfer_task(task_id, source, target, target_project_id, task_map, model_map)


# Copy models
for model_id in model_ids:
    transfer_model(model_id, source, target, target_project_id, model_map)

