from odoo import models,fields
class School(models.Model):
    _name='gems.school'
    _description='School belonging to GEMS'

    _sql_constraints = [('check_duplicates','UNIQUE(name)','Name already exsists')]
    name=fields.Char(string='name',required=True)
    establishment_date=fields.Date(string="Establishment Date",required=True)
    street_1 =fields.Char(string='Street 1')
    street_2 =fields.Char(string='street 2')
    city=fields.Char(string='City',required=True)
    state_id= fields.Many2one(comodel_name="res.country.state",string="State")
    country_id= fields.Many2one(comodel_name="res.country",string="Country",required=True)
    zip= fields.Char(string="Zip")
    faculty_member_ids=fields.One2many(string='Faculty',comodel_name='res.users',inverse_name='school_id')
    student_ids=fields.One2many(string='Students',comodel_name='res.users',inverse_name='school_id')
    classroom_ids=fields.One2many(string='Classrooms',comodel_name='gems.classroom',inverse_name='school_id')
    subject_ids=fields.Many2many(string='Subjects',comodel_name='gems_subject')
    session_ids=fields.One2many(string="Sessions",comodel_name='gems_session')
