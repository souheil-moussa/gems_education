from odoo import fields , models

class gemssubject(models.Model):
    _name = "gems.subject"
    _description = "Subject"

    name = fields.Char(string="Name", required=True)
    school_id = fields.Many2one(comodel_name="gems.school", string="School", required=True)
    book = fields.Char(string="Book")

    _sql_constraints = [('unique_subject_name_per_school','unique(name, school_id)','Subject name must be unique within the same school!')]
