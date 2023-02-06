from odoo import api, fields, models


class Project(models.Model):
    _inherit = 'project.project'

    _sql_constraints = [
        (
            'project_code_unique',
            'unique (project_code)',
            'Project with this code already exists!'
        ),
    ]

    project_code = fields.Char('Project tasks UID prefix')
    next_task_id = fields.Integer(
        'Next id for task', compute='_compute_next_id'
    )

    def _compute_next_id(self):
        self.next_task_id = 1


class Task(models.Model):
    _inherit = 'project.task'

    _sql_constraints = [
        (
            'task_uid_unique',
            'unique (task_uid)',
            'Task with this UID already exists!'
        ),
    ]

    task_uid = fields.Char('Task UID')

    @api.model_create_multi
    def create(self, vals_list):
        print(vals_list)
        projects = super().create(vals_list)
        return projects
