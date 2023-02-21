from odoo import fields, models


class UIDHistory(models.Model):
    _name = 'project.uid_history'
    _description = 'История тегов задач'
    _rec_name = 'old_uid'

    old_uid = fields.Char('Старый код задачи')
    task_id = fields.Many2one('project.task')
