import asyncio
import random
import string
import time
import json
from command_line.libs.core.harbor_lib import NestService 
from harborapi.models import UserGroup

async def create_group(group: dict):
    nest_service = NestService()
    client = nest_service.get_client_by_type(type="new")
    try:
        res = await client.create_usergroup(
                usergroup=UserGroup(
                    group_name=group["entity_name"],
                    ldap_group_dn=group["entity_name"].lower(),
                    group_type=group["group_type"]
                )
        )
    except Exception as e:
        print(e)

    print(f"res: {res}")
    return res


async def get_users_project(type: string, project_vals):
    nest_service = NestService()
    client = nest_service.get_client_by_type(type)
    try:
        return await client.get_project_members(
                project_name_or_id=project_vals
            )
    except Exception as e:
        print(e)

    # print(project_members)
    # return project_members

async def add_user_project(user: string, role_id: string, project: string):
    nest_service = NestService()
    client = nest_service.get_client_by_type(type="new")
    try:
        res = await client.add_project_member_user(
                project_name_or_id = project,
                username_or_id = user,
                role_id = role_id
        )
    except Exception as e:
        print(e)

    print(f"res: {res}")
    return res

async def add_group_project(group: string, role_id: string, project: string):
    nest_service = NestService()
    client = nest_service.get_client_by_type(type="new")
    try:
        res = await client.add_project_member_group(
                project_name_or_id = project,
                ldap_group_dn_or_id = group,
                role_id = role_id
        )
    except Exception as e:
        print(e)

    print(f"res: {res}")
    return res


async def update_user_project_role(user: string, role_id: string, project):
    nest_service = NestService()
    client = nest_service.get_client_by_type(type="new")
    try:
        res = await client.update_project_member_role(
                project_name_or_id = project,
                member_id = user,
                role = role_id
        )
    except Exception as e:
        print(e)

    print(f"res: {res}")
    return res


async def align_user(user, userdata, project) -> None:
    if isinstance(userdata["role_name"], dict):
        print(f"Updating User {user} to " + userdata["role_name"]["old_value"] + " into " + project)
        await update_user_project_role(userdata["id"], userdata["role_id"]["old_value"], project)
    else:
        print(f"Updating User {user} to " + userdata["role_name"] + " into " + project)
        if userdata["entity_type"] == 'g':
            print( "User {user} is a Group")
            userdata["group_type"] = 1
            print( "Add {user} as a Group")
            await create_group(userdata)

            print( "Group {user} added to {project}")
            await add_group_project(user.lower(), userdata["role_id"], project)
        else:
            await add_user_project(user, userdata["role_id"], project)
    # else:
    #     raise ValueError("Formato utente non supportato")
    return

async def align_users_project(type, project, dry) -> None:

    h1_users_map = {} 
    h2_users_map = {}
    _h1_project_members = await get_users_project(type="old", project_vals=project["old_id"])
    _h2_project_members = await get_users_project(type="new", project_vals=project["name"])
    for user in _h1_project_members:
        h1_users_map[user.entity_name] = json.loads(user.json())
        # h1_users_map[user.entity_name] = user.model_dump()
    for user in _h2_project_members:
        h2_users_map[user.entity_name] = json.loads(user.json())
        # h2_users_map[user.entity_name] = user.model_dump()
    project["changes_existing_users"] = {}
    project["new_users"] = {}
    for username, user_h1 in h1_users_map.items():
        if username in h2_users_map:
            # print("----------")
            # print(user_h1)
            user_h2 = h2_users_map[username]
            # print("----------")
            # print(user_h2)
            diff_fields = {}
            for key,value_h1 in user_h1.items():
                if key == "id" or key == "entity_id": 
                    continue
                value_h2 = user_h2[key]
                if value_h2 != value_h1:
                    diff_fields[key] = {"old_value": value_h1, "new_value": value_h2} 
            if diff_fields:
                # print("----------")
                # print("Reported Changes in Userbase:")
                # print(diff_fields)
                # print("----------")
                project["changes_existing_users"][username] = diff_fields
                project["changes_existing_users"][username]["id"] = user_h2["id"]
        else:
            project["new_users"][username] = user_h1
            
    # if(dry != True):
    #     if project["changes_existing_users"]:
    #         print("Start updating already knowed Users:")
    #         for user,userdata in project["changes_existing_users"].items():
    #             print("updating " + user)
    #             await align_user(user, userdata ,project["name"])
    #     else:
    #         print("No major Changes in user base:")

    if(dry != True):
        if project["new_users"]:
            print("Start adding new Users:")
            for user,userdata in project["new_users"].items():
                print("updating " +user)
                await align_user(user, userdata, project["name"])
        else:
            print("No Adding in user base:")

    return project 

    