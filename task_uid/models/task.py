from odoo import api, fields, models
from typing import Union


class Task(models.Model):
    _inherit = 'project.task'

    _sql_constraints = [
        (
            'task_uid_unique',
            'unique (task_uid)',
            'Task with this UID already exists!'
        ),
    ]

    task_uid = fields.Char('Код задачи')
    task_history_ids = fields.One2many(
        'project.uid_history', 'task_id', string='История кодов'
    )

    def _get_task_uid(self, project_id: int) -> Union[None, str]:
        project = self.env['project.project'].search([('id', '=', project_id)])

        if not (code := project.project_code):
            return None

        id = project.get_or_create_sequence().next_by_id()  

        return f'{code}-{id:0>3}'

    @api.model_create_single
    def create(self, vals):
        vals['task_uid'] = self._get_task_uid(vals['project_id'])

        return super(Task, self).create(vals)

    def write(self, vals: dict):
        if (vals.get("project_id") is None
                or vals['project_id'] == self.project_id.id):  # type: ignore
            return super(Task, self).write(vals)

        if self.task_uid:
            self.env['project.uid_history'].create({
                'old_uid': self.task_uid,
                'task_id': self.id,  # type: ignore
            })
            self.env.cr.commit()

        vals['task_uid'] = self._get_task_uid(vals['project_id'])

        return super(Task, self).write(vals)

    @api.depends('name', 'task_uid')
    def name_get(self):
        tasks = []

        for task in self:
            prefix = f'[{task.task_uid}] ' if task.task_uid else ''
            name = prefix + task.name  # type: ignore
            tasks.append((task.id, name))  # type: ignore

        return tasks
