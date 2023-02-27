from odoo import api, fields, models

from .project import Project


class Task(models.Model):
    _inherit = 'project.task'

    _sql_constraints = [
        (
            'task_uid_unique',
            'unique (task_uid)',
            'Task with this UID already exists!'
        ),
    ]

    task_uid = fields.Char('Task code')
    task_history_ids = fields.One2many(
        'project.task.history', 'task_id', string='History of tasks code'
    )

    def _get_project(self, project_id: int) -> Project:
        return self.env['project.project'].search([('id', '=', project_id)])

    @api.model_create_single
    def create(self, vals: dict):
        vals['task_uid'] = self._get_project(vals['project_id']).get_task_uid()

        return super(Task, self).create(vals)

    def write(self, vals: dict):
        if vals.get("project_id") and vals['project_id'] != self.project_id.id:
            if self.task_uid:
                self.env['project.task.history'].create({
                    'old_uid': self.task_uid,
                    'task_id': self.id,
                })

            vals['task_uid'] = self._get_project(
                vals['project_id']
            ).get_task_uid()

        return super(Task, self).write(vals)

    @api.depends('name', 'task_uid')
    def name_get(self):
        tasks = []

        for task in self:
            prefix = f'[{task.task_uid}] ' if task.task_uid else ''
            name = f'{prefix} {task.name}'
            tasks.append((task.id, name))

        return tasks
