import asyncio
import random
import string
import time
import json
from datetime import datetime
from command_line.libs.core.harbor_lib import NestService 
from harborapi.models import ProjectReq, ProjectMetadata

async def get_project(type: string, project_name_or_id):
    nest_service = NestService()
    client = nest_service.get_client_by_type(type)
    try:
        return await client.get_project(
            project_name_or_id=project_name_or_id
        )
    except Exception as e:
        print(e)

async def get_projects(type: string):
    nest_service = NestService()
    client = nest_service.get_client_by_type(type)
    try:
        return await client.get_projects()
    except Exception as e:
        print(e)

async def update_project(type: string, project_vals: dict):
    nest_service = NestService()
    client = nest_service.get_client_by_type(type)
    project_object = ProjectReq()
    try:
        return await client.update_project(
            project_name_or_id=project_vals.name,
            project=project_object
        )
    except Exception as e:
        print(e)

async def set_project_metadata(type: string, project_id: string, meta_name: string, meta_value: string):
    nest_service = NestService()
    client = nest_service.get_client_by_type(type="new")
    try:
        res =  await client.set_project_metadata(
            project_name_or_id= project_id,
            metadata = meta_value
        )
        print(res)
    except Exception as e:
        print(e)
        
async def update_project_metadata(type: string, project_id: string, meta_name: string, meta_value: string):
    nest_service = NestService()
    client = nest_service.get_client_by_type(type="new")
    try:
        res =  await client.update_project_metadata_entry(
            project_name_or_id= project_id,
            metadata_name = meta_name,
            metadata = meta_value
        )
        print(res)
    except Exception as e:
        print(e)

async def align_meta(project_id: string, meta_name: string, meta_value: string, h2_meta_value: dict):
    res = {}
    model_meta = {}

    
    print( meta_name +" : " +str(h2_meta_value))
    if h2_meta_value:
        print("Start update metadata " + meta_name +"  to: " +str(meta_value))
        model_meta[meta_name] = meta_value
        print(ProjectMetadata.model_validate(model_meta))
        await update_project_metadata(
            type="new", project_id=project_id, meta_name=meta_name, meta_value=model_meta
        )
    else:
        print("Start Set metadata " + meta_name +" to: " +str(meta_value))
        model_meta[meta_name] = meta_value
        print(ProjectMetadata.model_validate(model_meta))
        await set_project_metadata(
            type="new", project_id=project_id, meta_name=meta_name, meta_value=model_meta
        )

    return res


async def align_metadatas_project(project, dry) -> None:
    now = datetime.now()
    output = {"metas_holded": {}, "metas_to_sync": {}, "data": now.strftime("%Y-%m-%d %H:%M:%S"), "id": None, "name": None}

    output["id"] = project['new_id']
    output["name"] = project['name']
    output["old_metas"]  = project['old_metas'].__dict__
    output["new_metas"]  = project['new_metas'].__dict__
    for meta, meta_value in project["old_metas"].__dict__.items():
        h2_meta_value = getattr(project['new_metas'], meta)
        if meta_value == h2_meta_value:
            output["metas_holded"][meta] = meta_value
        else:
            output["metas_to_sync"][meta] = meta_value

    if(dry != True):
        if output["metas_to_sync"]:
            print("Start to align metadatas:")
            for meta, meta_value in output["metas_to_sync"].items():
                if meta_value:
                    output["Reponse"] = await align_meta(
                        project_id=output["id"], 
                        meta_name=meta, 
                        meta_value=meta_value,
                        h2_meta_value=getattr(project['new_metas'], meta)
                    )
                else:
                    continue
            
    return output 
