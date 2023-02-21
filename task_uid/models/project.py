from typing import Union
from odoo import api, fields, models, _

import logging

logger = logging.getLogger()


class TaskHistory(models.Model):
    _name = 'project.task_history'
    _description = 'История тегов задач'
    _rec_name = 'old_uid'

    old_uid = fields.Char('Старый код задачи')
    task_id = fields.Many2one('project.task')


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

    def get_or_create_sequence(self):
        self.ensure_one()
        code = f'project.project.project_code.{self.project_code}'
        sequence = self.env['ir.sequence'].search([('code', '=', code)])

        if not sequence:
            name = f'project {self.name}'  # type: ignore
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

    def _search_task_uid(self, operator, value):
        # query = """
        #     SELECT task.task_uid
        #     FROM project_task
        #     WHERE partners.name ILIKE %s
        # """
        # return [('id', 'inselect', (query, [f'%{value}%']))]
        logger.warning('OK')
        current_ids = self.env['project.task'].search(
            [('task_uid', 'in', value)])
        old_ids = self.env['project.task_history'].search(
            [('old_uid', 'in', value)])
        return [('id', 'in', old_ids)]

    task_uid = fields.Char('Код задачи', search='_search_task_uid')
    task_history_ids = fields.One2many(
        'project.task_history', 'task_id', string='История кодов'
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
            self.env['project.task_history'].create({
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
