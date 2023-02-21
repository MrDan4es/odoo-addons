from odoo import fields, models


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

