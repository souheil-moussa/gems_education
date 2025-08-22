from odoo import models, fields

class gemsclassroom(models.Model):
    _name = "gems.classroom"
    _description = "Classroom"

    name = fields.Char(string="Name", required=True)
    school_id = fields.Many2one(comodel_name="gems.school", string="School", required=True)
    capacity = fields.Integer(string="Capacity", required=True, default=5)
    has_projector = fields.Boolean(string="Has Projector?")
    has_smart_board = fields.Boolean(string="Has Smart Board?")

    _sql_constraints = [('unique_classroom_name_per_school','unique(name, school_id)','Classroom name must be unique within the same school!')]