from odoo import fields, models


class TaskHistory(models.Model):
    _name = 'project.task.history'
    _description = 'Task tag history model'
    _rec_name = 'old_uid'

    old_uid = fields.Char('Previous task code')
    task_id = fields.Many2one('project.task')
