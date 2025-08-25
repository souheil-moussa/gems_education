from odoo import models,fields,api,_
from datetime import date
class User(models.Model):
    _inherit='res.users'
    
    school_id=fields.Many2one(comodel_name='gems.school',string='School')
    gems_role=fields.Selection(string="Role", related='partner_id.gems_role',readonly=False)
    session_nb=fields.Integer(compute='count_sessions')
    session_ids=fields.Many2many(comodel_name='gems.session')



    dob = fields.Date(string='Date of Birth',related='partner_id.dob',readonly=False)
    gender = fields.Selection(related='partner_id.gender',string='Gender',readonly=False)
    age_years = fields.Integer(string='Age (Years)', compute='_compute_age')
    age_months = fields.Integer(string='Age (Months)', compute='_compute_age')
    age = fields.Char(string='Age', compute='_compute_age')
    student_id=fields.Char(string='Student Id',related='partner_id.student_id',readonly=False)
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
    @api.model_create_multi
    def create(self, vals_list):
        seq_model = self.env['ir.sequence']

        # Precompute student_id per record BEFORE create (no extra write, no recursion)
        for vals in vals_list:
            role = vals.get('gems_role')
            if role == 'student' and not vals.get('student_id'):
                gender = vals.get('gender')  # may be None if not passed
                if gender == 'male':
                    prefix = 'M'
                elif gender == 'female':
                    prefix = 'F'
                else:
                    prefix = 'X'
                seq = seq_model.next_by_code('gems.student') or ''
                vals['student_id'] = f"{prefix}{seq}"

        users = super().create(vals_list)
        return users
    
    def write(self, vals):
        res = super().write(vals)  # apply normal changes first

        for user in self:
            if user.gems_role == 'student' and not user.student_id:
                prefix = (
                    'M' if user.gender == 'male'
                    else 'F' if user.gender == 'female'
                    else 'X'
                )
                seq = self.env['ir.sequence'].next_by_code('gems.student')
                super(User, user).write({'student_id': f"{prefix}{seq}"})
        return res

