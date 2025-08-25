from odoo import models,fields,api,_
class Partner(models.Model):
    _inherit='res.partner'
    gems_role=fields.Selection(selection=[('faculty','Faculty'),('student','Student')])
    dob = fields.Date(string='Date of Birth')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string='Gender'
    ) 
    student_id=fields.Char(string='Student Id')
