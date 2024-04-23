from setuptools import setup, find_packages

setup(
    name='command_line',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'projects-users-align = command_line.scripts.users:all_projects_users',
            'project-users-align = command_line.scripts.users:project_users',
            'project-user-align = command_line.scripts.users:project_user',
        ],
    },
)