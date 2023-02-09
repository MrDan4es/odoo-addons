from odoo import api, fields, models, _


class Project(models.Model):
    _inherit = 'project.project'

    _sql_constraints = [
        (
            'project_code_unique',
            'unique (project_code)',
            'Project with this code already exists!'
        ),
    ]

    project_code = fields.Char('Код задач')
    project_task_sequence = fields.Many2one('ir.sequence')

    def create_sequence(self):
        self.ensure_one()
        code = f'project.project.project_code.{self.project_code}'
        sequence = self.env['ir.sequence'].search([('code', '=', code)])
        if not sequence:
            name = f'project {self.name}'
            sequence = self.env["ir.sequence"].sudo().create({
                'code': code,
                'name': name
            })
            self.sudo().project_task_sequence = sequence
            return sequence


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

    @api.model_create_single
    def create(self, vals):
        project = self.env['project.project'].search(
            [('id', '=', vals['project_id'])]
        )
        code = project.project_code
        if code:
            sequence = self.env['ir.sequence'].search([(
                'code', '=', f'project.project.project_code.{code}'
            )])
            if not sequence:
                sequence = project.create_sequence()
            id = sequence.next_by_id()
            vals['task_uid'] = f'{project.project_code}-{id:0>3}'

        return super(Task, self).create(vals)

    @api.depends('name', 'task_uid')
    def name_get(self):
        tasks = []

        for task in self:
            prefix = f'[{task.task_uid}] ' if task.task_uid else ''
            name = prefix + task.name
            tasks.append((task.id, name))

        return tasks
