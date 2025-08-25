from odoo import models,fields,api

class User(models.Model):
    _inherit='res.users'
    
    school_id=fields.Many2one(comodel_name='gems.school',string='School')
    gems_role=fields.Selection(selection=[('faculty','Faculty'),('student','Student')])
    session_nb=fields.Integer(compute='count_sessions')
    session_ids=fields.Many2many(comodel_name='gems.session')
    def user_session_button_action(self):
        self.ensure_one()
        return{
        'type': 'ir.actions.act_window',
        'name': 'Sessions',
        'view_mode': 'list',
        'res_model': 'gems.session',
        'domain': ['|',('teacher_id', '=', self.id),('student_ids','in',self.id)],
        'context': "{'create': False}"
        }
    @api.depends('session_ids')
    def count_sessions(self):
        for record in self:
            count = 0
            if record.session_ids:
                for room in record.session_ids:
                    count+= 1
            record.session_nb = count

