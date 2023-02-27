from typing import Union

from odoo import fields, models
from odoo.addons.base.models.ir_sequence import IrSequence


class Project(models.Model):
    _inherit = 'project.project'

    _sql_constraints = [
        (
            'project_code_unique',
            'unique (project_code)',
            'Project with this code already exists!'
        ),
    ]

    project_code = fields.Char('Project code')
    project_task_sequence = fields.Many2one('ir.sequence')

    def _get_or_create_sequence(self) -> IrSequence:
        """
        Checks if sequence exists by code, creates if not
        Returns: `project_task_sequence`: IrSequence
        """
        self.ensure_one()
        code = f'project.project.project_code.{self.project_code}'
        sequence = self.env['ir.sequence'].search([('code', '=', code)])

        if not sequence:
            sequence = self.env["ir.sequence"].sudo().create({
                'code': code,
                'name': f'project {self.name}'  # type: ignore
            })
            self.sudo().project_task_sequence = sequence

        return sequence

    def get_task_uid(self) -> Union[None, str]:
        """
        Returns:    
            - `None`, if `project_code` not exist
            - str: `{project_code}-{int}`. Example : `RYD-001`
        """
        if not self.project_code:
            return None

        id = self._get_or_create_sequence().next_by_id()

        return f'{self.project_code}-{id:0>3}'
