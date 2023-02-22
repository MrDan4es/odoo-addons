from odoo import fields, models
from typing import Union


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

    def _get_or_create_sequence(self):
        self.ensure_one()

        if self.project_task_sequence:
            return self.project_task_sequence

        code = f'project.project.project_code.{self.project_code}'
        sequence = self.env["ir.sequence"].sudo().create({
            'code': code,
            'name': f'project {self.name}'  # type: ignore
        })
        self.sudo().project_task_sequence = sequence

        return sequence

    def get_task_uid(self) -> Union[None, str]:
        if not self.project_code:
            return None

        id = self._get_or_create_sequence().next_by_id()

        return f'{self.project_code}-{id:0>3}'
