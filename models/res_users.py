from odoo import models,fields

class User(models.Model):
    _inherit='res.users'
    
    school_id=fields.Many2one(comodel_name='gems.school',string='School')
    gems_role=fields.Selection(selection=[('faculty','Faculty'),('student,Student')])
