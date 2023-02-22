from odoo import api, fields, models


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

    def _get_project(self, project_id):
        return self.env['project.project'].search([('id', '=', project_id)])

    @api.model_create_single
    def create(self, vals):
        vals['task_uid'] = self._get_project(vals['project_id']).get_task_uid()
        
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

        vals['task_uid'] = self._get_project(vals['project_id']).get_task_uid()

        return super(Task, self).write(vals)

    @api.depends('name', 'task_uid')
    def name_get(self):
        tasks = []

        for task in self:
            prefix = f'[{task.task_uid}] ' if task.task_uid else ''
            name = prefix + task.name  # type: ignore
            tasks.append((task.id, name))  # type: ignore

        return tasks
