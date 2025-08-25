from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Grade(models.Model):
    _name = "gems.grade"
    _description = "School Grade"
    _rec_name = "name"

    name = fields.Char(string="Grade Name", required=True)
    school_id = fields.Many2one(comodel_name="gems.school", string="School", required=True, ondelete="cascade")

    _sql_constraints = [('unique_grade_per_school', 'unique(name, school_id)', 'Grade name must be unique within the same school!')]

    