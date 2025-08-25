from odoo import models,fields,api,_
from datetime import date
class User(models.Model):
    _inherit='res.users'
    
    school_id=fields.Many2one(comodel_name='gems.school',string='School')
    gems_role=fields.Selection(selection=[('faculty','Faculty'),('student','Student')])
    session_nb=fields.Integer(compute='count_sessions')
    session_ids=fields.Many2many(comodel_name='gems.session')



    dob = fields.Date(string='Date of Birth')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string='Gender'
    )
    age_years = fields.Integer(string='Age (Years)', compute='_compute_age')
    age_months = fields.Integer(string='Age (Months)', compute='_compute_age')
    age = fields.Char(string='Age', compute='_compute_age')

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
    
    @api.depends('dob')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            y = m = 0
            if rec.dob:
                if rec.dob > today:
                    rec.age_years = 0
                    rec.age_months = 0
                    rec.age = _("Invalid DOB (in the future)")
                    continue
                y = today.year - rec.dob.year
                m = today.month - rec.dob.month
                if today.day < rec.dob.day:
                    m -= 1
                if m < 0:
                    y -= 1
                    m += 12
            rec.age_years = y
            rec.age_months = m
            rec.age = f"{y}y {m}m" if rec.dob else False

    @api.onchange('gems_role')
    def _onchange_gems_role_clear_student_fields(self):
         if self.gems_role != 'student':
              self.dob = False
              self.gender = False
