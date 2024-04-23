import anyio
import asyncclick as click
from command_line.libs.projects_service import get_projects, align_metadatas_project
from command_line.libs.utils.dumper import FileUtility



@click.command()
@click.option('--dry', default=False, help='Want just a lookup before do the alignment. Output: outputs/users-UniForm.json')
@click.option('--type',default="Full", prompt='What kind of migration you want to do, Full / Users / Groups / OnlyDev',
              help='What kind of migration you want to do, Full / Users / Groups / OnlyDev')
async def all_metadata_projects(dry, type):
    """Utility script for align Users Setup from Old Harbor to new Harbor"""
    click.echo('Utility script for align Users for each project synced from Old Harbor to new Harbor')
    h1_api = "old"
    result={}
    project_values={}
    if(h1_api == "old"):
        try:
            projects_h1 = await get_projects(type="old")
            projects_h2 = await get_projects(type="new")
            project_map_h1 = dict(map(lambda project: (project.name, (project.project_id, project.metadata)), projects_h1))
            project_map_h2 = dict(map(lambda project: (project.name, (project.project_id, project.metadata)), projects_h2))
            # project_map_h2 = dict(map(lambda project: (project.name, project.project_id), projects_h2))
        except Exception as e:
            print(f"Error Catching the projects: {e}")
            exit()
        
        # print(project_map_h1)
        for project in project_map_h1:
            if project in project_map_h2:
                project_values = {
                    "name": project,
                    "old_id": project_map_h1[project][0], 
                    "new_id": project_map_h2[project][0], 
                    "old_metas": project_map_h1[project][1],
                    "new_metas": project_map_h2[project][1],
                }

                try:
                    # print(project_values)
                    result[project] = await align_metadatas_project(project_values, dry)
                except Exception as e:
                    print(e)

    
    FileUtility.dump_json(data=result, invoke="metadata",path_dir="outputs/")

@click.command()
@click.option('--dry', default=False, help='Want just a lookup before do the alignment. Output: outputs/users-UniForm.json')
@click.option('--project', default="library", help='THe name of the project you want to sync the users')
@click.option('--type',default="Full", prompt='What kind of migration you want to do, Full / Users / Groups / OnlyDev',
              help='What kind of migration you want to do, Full / Users / Groups / OnlyDev')
async def all_metadata_project(dry, project, type):
    """Utility script for align Users Setup from Old Harbor to new Harbor"""
    click.echo('Utility script for align Users Setup from Old Harbor to new Harbor')
    h1_api = "old"
    project_values={}
    if(h1_api == "old"):
        try:
            projects_h1 = await get_projects(type="old")
            # print(projects_h1)
            project_map_h1 = dict(map(lambda project: (project.name, project.project_id), projects_h1))
            project_values = {
                "name": project,
                "old_id": project_map_h1[project]
            }
        except Exception as e:
            print(f"Error Catching the project: {e}")
            exit()
    else:
        project_values={
            "name": project
        }
    
    res={}
    # try:
    #     # res = await align_users_project(type, project_values, dry)
    # except Exception as e:
    #     print(e)
    
    # FileUtility.dump_json(data=res, invoke="metadata",path_dir="outputs/")

if __name__ == '__main__':
    all_metadata_projects()