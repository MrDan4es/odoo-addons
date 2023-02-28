from odoo.http import Controller, request, route
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect


class TaskUrlController(Controller):

    @route('/task/<string:uid>', type='http', auth='public', website=True)
    def get_task_url(self, uid, **kw):
        task_id = None
        task_model = request.env['project.task'].sudo()
        task = task_model.search([('task_uid', '=ilike', uid)], limit=1)

        if not task:
            history_model = request.env['project.task.history'].sudo()
            history = history_model.search(
                [('old_uid', '=ilike', uid)], limit=1
            )

            if history:
                task_id = history.task_id.id
        else:
            task_id = task.id

        if task_id:
            return redirect(f'/web#id={task_id}&model=project.task')

        raise NotFound()