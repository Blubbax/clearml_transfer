from clearml import Dataset

def transfer_task(id, source, target, target_project, task_map, model_map):

    # Check if already copied (e.g. parent is also in list)
    if id in task_map:
        return task_map[id]

    # Get task
    task = source.tasks.get_by_id(task=id)

    # Prepare task
    if task.parent != None:
        if id in task_map:
            task.parent = task_map[id]
        else:
            task.parent = transfer_task(task.parent, source, target, target_project, task_map, model_map)


    task.tags.append('LNU TRANSFER')

    for model in task.models.input:
        model_id = model.model
        model.model = transfer_model(model_id, source, target, target_project, model_map)
        print(f'INFO: {model_id} transferred')

    for model in task.models.output:
        model_id = model.model
        model.model = transfer_model(model_id, source, target, target_project, model_map)
        print(f'INFO: {model_id} transferred')

       
    for artifact in task.execution.artifacts:
        # print(artifact)
        # TODO artifact.uri --> copy to another location and update
        pass

    # The following queries are used to get the metrics data
    # and scalars. But I have not found a solution to store it in the new model
    # events = source.events.get_task_events(task=id)
    # events = source.events.get_task_log(task=id)
    # events = source.events.get_task_latest_scalar_values(task=id)
    # events = source.events.get_task_metrics(tasks=[id])
    # events = source.events.get_task_plots(task=id)
    # events = source.events.get_task_single_value_metrics(tasks=[id])

    # Store task
    insert = target.tasks.create(
        comment=task.comment,
        configuration=task.configuration,
        container=task.container,
        execution=task.execution,
        hyperparams=task.hyperparams,
        models=task.models,
        name=task.name,
        output_dest= task.output_dest if hasattr(task, 'output_dest') else None,
        parent=task.parent,
        project=target_project,
        script=task.script,
        system_tags=task.system_tags,
        tags=task.tags,
        type=task.type
    )

    # Add to task map
    task_map[id] = insert.id
    
    # new_task = target.tasks.get_by_id(insert.id)

    # Return new id
    return insert.id


def transfer_model(id, source, target, target_project, model_map):
   
    # Check if already copied
    if id in model_map:
        return model_map[id]

    model = source.models.get_by_id(model=id)

    if model.parent != None:
        if id in model_map:
            model.parent = model_map[id]
        else:
            model.parent = transfer_model(model.parent, source, target, target_project, model_map)

    model.tags.append('LNU TRANSFER')

    # TODO copy artifact from model.uri to new location and update uri

    insert = target.models.create(
        comment=model.comment,
        design=model.design,
        framework=model.framework,
        labels=model.labels,
        name=model.name,
        parent=model.parent,
        project=target_project,
        public=model.public if hasattr(model, 'public') else False,
        ready=model.ready,
        system_tags=model.system_tags,
        tags=model.tags,
        task=model.task,
        uri=model.uri
    )

    model_map[id] = insert.id
    
    return insert.id

def transfer_dataset(uri, project_name):

    # How can I select the target ClearML environment?
    dataset = Dataset.create(
        dataset_name="iris_processed",
        dataset_project="Iris"
    )

    dataset.add_files(uri)
    dataset.upload()
    dataset.finalize()