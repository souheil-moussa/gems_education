from odoo import models, fields, api
from datetime import date, datetime

class GemsSession(models.Model):
    _name = "gems.session"
    _description = "Gems Session"
    _inherit = ["mail.thread", "mail.activity.mixin"]



    name = fields.Char(string="Session Name", required=True)
    grade_id = fields.Many2one(comodel_name="gems.grade", string="Grade", required=True)
    subject_id = fields.Many2one(comodel_name='gems.subject', string='Subject', required=True)
    classroom_id = fields.Many2one(comodel_name='gems.classroom', string='Classroom', required=True)
    teacher_id = fields.Many2one(comodel_name='res.users', string='Teacher', required=True)
    year = fields.Integer(string="Year", required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    start_time = fields.Datetime(string="Start Time", required=True)
    end_time = fields.Datetime(string="End Time", required=True)
    student_ids = fields.Many2many(comodel_name='res.users', string='Students') 
    school_id = fields.Many2one(comodel_name='gems.school')
    
    is_active=fields.Boolean(string='Active', compute='_is_active_')


    @api.constrains('start_time','end_time')
    def _check_datetime(self):
        for record in self:
            if record.start_time > record.end_time:
                raise ValidationError("Start Time cannot be after End Time")
    def write(self, vals):
        res = super().write(vals)
        if "student_ids" in vals:
            self._notify_new_students(vals["student_ids"])
        return res

    def _notify_new_students(self, student_commands):
        """
        Only notify newly added students (not removed).
        """
        for session in self:

            new_student_ids = []
            for command in student_commands:
                if command[0] == 4:  
                    new_student_ids.append(command[1])
                elif command[0] == 6: 
                    current = set(session.student_ids.ids)
                    new = set(command[2])
                    new_student_ids.extend(list(new - current))

            if not new_student_ids:
                continue

            for student in self.env["res.users"].browse(new_student_ids):

                message = (
                    "You have been registered for the subject %s. "
                    "The session starts at %s and the timings are from %s to %s. "
                    "Please check your updated schedule.<br/><br/>Regards, %s"
                ) % (
                    session.subject_id.name,
                    session.start_date,
                    session.start_time,
                    session.end_time,
                    session.teacher_id.name,
                )


                session.message_post(
                    body=message,
                    partner_ids=[student.partner_id.id],
                )

                self.env["mail.activity"].create({
                    "res_model_id": self.env["ir.model"]._get_id("gems.session"),
                    "res_id": session.id,
                    "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                    "summary": "Review New Course",
                    "date_deadline": date.today(),
                    "user_id": student.id,
                    "note": message,
                })
    def _is_active_(self):
        for record in self:
            if date.today()>record.start_date and date.today()<record.end_date:
                record.is_active = True
            else:
                record.is_active= False
