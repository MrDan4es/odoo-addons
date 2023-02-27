# type: ignore
{
    'name': 'task_uid',
    'version': '16.0.0.2',
    'summary': 'Module for project tags and task uids with history',
    'category': 'Generic Modules/Others',
    'author': 'RYDLAB',
    'maintainer': 'RYDLAB',
    'website': 'https://www.rydlab.ru',
    'license': 'GPL-3',
    'depends': [
        'project',
    ],
    'data': [
        "security/ir.model.access.csv",
        'views/project_view.xml'
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
