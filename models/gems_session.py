from odoo import models, fields
from odoo.exceptions import ValidationError

class GemsSession():
    _name = "gems.session"
    _description = "Gems Session"

    subject_id = fields.Many2one('gems.subject', string='Subject',required=True)
    classroom_id = fields.Many2one('gems.classroom', string='classroom',required=True)
    teacher_id = fields.Many2one('res.users', string='Teacher',required=True)
    year = fields.Integer(string="Year",required=True)
    start_date = fields.Date('Start Date',required=True)
    end_date = fields.Date('End Date',required=True)
    start_time = fields.string(string="Start Time (HH:MM)",required=True)
    end_time = fields.string(string="End Time (HH:MM)",required=True)
    students_ids = fields.Many2many('gems.student', string='Students')
