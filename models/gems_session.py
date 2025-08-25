from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GemsSession(models.Model):
    _name = "gems.session"
    _description = "Gems Session"

    subject_id = fields.Many2one(comodel_name='gems.subject', string='Subject',required=True)
    classroom_id = fields.Many2one(comodel_name='gems.classroom', string='classroom',required=True)
    teacher_id = fields.Many2one(comodel_name='res.users', string='Teacher',required=True)
    year = fields.Integer(string="Year",required=True)
    start_date = fields.Date('Start Date',required=True)
    end_date = fields.Date('End Date',required=True)
    start_time = fields.Datetime(string="Start Time (HH:MM)",required=True)
    end_time = fields.Datetime(string="End Time (HH:MM)",required=True)
    student_ids = fields.Many2many(comodel_name='gems.school', string='Students')
    school_id = fields.Many2one(comodel_name='gems.school')

    @api.constrains('start_time', 'end_time')
    def _check_datetime(self):
        """Ensure start_time is before end_time"""
        for record in self:
            if record.start_time and record.end_time:
                if record.start_time > record.end_time:
                    raise ValidationError("Start Time cannot be after End Time.")