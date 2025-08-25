from odoo import models,fields,api
class School(models.Model):
    _name='gems.school'
    _description='School belonging to GEMS'

    _sql_constraints = [('check_duplicates','UNIQUE(name)','Name already exsists')]
    name=fields.Char(string='Name',required=True)
    establishment_date=fields.Date(string="Establishment Date",required=True)
    street_1 =fields.Char(string='Street 1')
    street_2 =fields.Char(string='Street 2')
    city=fields.Char(string='City',required=True)
    state_id= fields.Many2one(comodel_name="res.country.state",string="State")
    country_id= fields.Many2one(comodel_name="res.country",string="Country",required=True)
    zip= fields.Char(string="Zip")
    faculty_member_ids=fields.One2many(string='Faculty',comodel_name='res.users',inverse_name='school_id')
    student_ids=fields.One2many(string='Students',comodel_name='res.users',inverse_name='school_id')
    classroom_ids=fields.One2many(string='Classrooms',comodel_name='gems.classroom',inverse_name='school_id')
    subject_ids=fields.Many2many(string='Subjects',comodel_name='gems.subject')
    session_ids=fields.One2many(string="Sessions",comodel_name='gems.session',inverse_name='school_id')

    classroom_nb=fields.Integer(compute='count_classrooms')
    subject_nb=fields.Integer(compute='count_subjects')
    session_nb=fields.Integer(compute='count_sessions')
    faculty_nb=fields.Integer(compute='count_faculty')
    student_nb=fields.Integer(compute='count_students')

    @api.depends('classroom_ids')
    def count_classrooms(self):
        for record in self:
            count = 0
            if record.classroom_ids:
                for room in record.classroom_ids:
                    count+= 1
            record.classroom_nb = count

    @api.depends('subject_ids')
    def count_subjects(self):
        for record in self:
            count = 0
            if record.subject_ids:
                for room in record.subject_ids:
                    count+= 1
            record.subject_nb = count

    @api.depends('session_ids')
    def count_sessions(self):
        for record in self:
            count = 0
            if record.session_ids:
                for room in record.session_ids:
                    count+= 1
            record.session_nb = count
    @api.depends('faculty_member_ids')
    def count_faculty(self):
        for record in self:
            count = 0
            if record.faculty_member_ids:
                for room in record.faculty_member_ids:
                    count+= 1
            record.faculty_nb = count
    @api.depends('student_ids')
    def count_student(self):
        for record in self:
            count = 0
            if record.student_ids:
                for room in record.student_ids:
                    count+= 1
            record.student_nb = count
    def subject_button_action(self):


        self.ensure_one()
        return{
        'type': 'ir.actions.act_window',
        'name': 'Subjects',
        'view_mode': 'list',
        'res_model': 'gems.subject',
        'domain': [('school_id', '=', self.id)],
        'context': "{'create': False}"
        }
    def session_button_action(self):

        self.ensure_one()
        return{
        'type': 'ir.actions.act_window',
        'name': 'Sessions',
        'view_mode': 'list',
        'res_model': 'gems.session',
        'domain': [('school_id', '=', self.id)],
        'context': "{'create': False}"
        }
    def faculty_button_action(self):

        self.ensure_one()
        return{
        'type': 'ir.actions.act_window',
        'name': 'Faculty',
        'view_mode': 'list',
        'res_model': 'res.user',
        'domain': [('school_id', '=', self.id),('gems_role','=','faculty')],
        'context': "{'create': False}"
        }
    def student_button_action(self):

        self.ensure_one()
        return{
        'type': 'ir.actions.act_window',
        'name': 'Students',
        'view_mode': 'list',
        'res_model': 'res.user',
        'domain': [('school_id', '=', self.id),('gems_role','=','student')],
        'context': "{'create': False}"
        }
    def classroom_button_action(self):

        self.ensure_one()
        return{
        'type': 'ir.actions.act_window',
        'name': 'Classrooms',
        'view_mode': 'list',
        'res_model': 'gems.classroom',
        'domain': [('school_id', '=', self.id)],
        'context': "{'create': False}"
        }
