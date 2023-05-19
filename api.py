from clearml.backend_api.session.client import APIClient
from clearml.backend_api.session.client import StrictSession
from clearml.backend_api.session import Session
from utils import transfer_model, transfer_task
from clearml import TaskTypes
import sys
import getopt
import argparse

# **********************************************************************
#                               Arguments
# **********************************************************************

# This is intended to be used be the LNU contact person.
# Therefore, the LNU environment is probably the local installed version.
# This connection is established by using the local client configuration
# The connection to the other instance can be established by passing the
# client credentials.

api_conf_source = ''
api_target_host = ''
api_target_api_key = ''
api_target_secret_key = ''
target_project_name = "LNU Project"

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=str)
parser.add_argument('--target-host', type=str)
parser.add_argument('--target-api-key', type=str)
parser.add_argument('--target-secret', type=str)
parser.add_argument('--project', type=str)

args = parser.parse_args()

api_conf_source = args.source
api_target_host = args.target_host
api_target_api_key = args.target_api_key
api_target_secret_key = args.target_secret
target_project_name = args.project

# **********************************************************************
#                         Task and Model IDs
# **********************************************************************

# Models which are connected to tasks do not need to be added to the list

task_ids = [
    '5bd8f005e7c2444d95b4c2115b15598f',
    '499994df52df4fe19e00c481ca948588',
    'd4a17dc2ea8547ed9e78d4f4420e4241'
]

model_ids = []

# Constants and Variables
transfer_tag_name = "LNU TRANSFER"
task_map = dict()
model_map = dict()


# **********************************************************************
#                           Setup Connections
# **********************************************************************

# Setup source connection
session_source = StrictSession(config_file=api_conf_source)

# Setup target connection
# Two strict session objects does not work 
# An alternative connection pproach was required
session_target = Session(
    api_key=api_target_api_key,
    secret_key=api_target_secret_key,
    host=api_target_host
)

source = APIClient(session=session_source)
target = APIClient(session=session_target)

# **********************************************************************
#                         Execute Transfer
# **********************************************************************

# Check if target project exists, otherwise create it
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

