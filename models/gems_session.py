from odoo import models, fields
from odoo.exceptions import ValidationError

from odoo import api

class GemsSession(models.Model):
    _name = "gems.session"
    _description = "Gems Session"


    name = fields.Char(string="Session Name", required=True)
    grade_id = fields.Many2one(comodel_name="gems.grade", string="Grade", required=True)

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

    @api.model
    def create(self, vals):
        session = super().create(vals)
        session._create_student_activities(vals.get('student_ids', []))
        return session

    def write(self, vals):
        res = super().write(vals)
        if 'student_ids' in vals:
            self._create_student_activities(vals.get('student_ids'))
        return res

    def _create_student_activities(self, student_ids_list):
        student_ids = []
        if student_ids_list:
            for cmd in student_ids_list:
                if isinstance(cmd, tuple):
                    if cmd[0] in (4, 6):  
                        student_ids.extend(cmd[2] if len(cmd) > 2 else [cmd[1]])
                else:
                    student_ids.append(cmd)
        
        for student_id in student_ids:
            student = self.env['res.users'].browse(student_id)
            if student:
                self.env['mail.activity'].create({
                    'res_model_id': self.env['ir.model']._get('res.users').id,
                    'res_id': student.id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': 'Review New Course',
                    'date_deadline': fields.Date.today(),
                    'user_id': student.id,
                    'note': (
                        f"You have been registered for the subject {self.subject_id.name}. "
                        f"The session starts at {self.start_date} and the timings are from {self.start_time} to {self.end_time}. "
                        f"Please check your updated schedule. Regards, {self.teacher_id.name}."
                    )
                })
