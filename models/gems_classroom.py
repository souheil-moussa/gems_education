from odoo import models, fields,api

class gemsclassroom(models.Model):
    _name = "gems.classroom"
    _description = "Classroom"

    name = fields.Char(string="Name", required=True)
    school_id = fields.Many2one(comodel_name="gems.school", string="School", required=True)
    capacity = fields.Integer(string="Capacity", required=True, default=5)
    has_projector = fields.Boolean(string="Has Projector?")
    has_smart_board = fields.Boolean(string="Has Smart Board?")
    session_nb=fields.Integer(compute='count_sessions')

    session_ids=fields.One2many(comodel_name='gems.session',inverse_name='classroom_id')
    _sql_constraints = [('unique_classroom_name_per_school','unique(name, school_id)','Classroom name must be unique within the same school!')]
    
    def classroom_session_button_action(self):
        self.ensure_one()
        return{
        'type': 'ir.actions.act_window',
        'name': 'Sessions',
        'view_mode': 'list',
        'res_model': 'gems.session',
        'domain': [('classroom_id' ,'=', self.id)],
        'context': "{'create': False}"
        }
    @api.depends('session_ids')
    def count_sessions(self):
        for record in self:
            count = 0
            if record.session_ids:
                for room in record.session_ids:
                    count+= 1
            record.session_nb = count
    @api.constrains('capacity')
    def _check_capacity_not_full(self):
        for record in self:
            if record.capacity < 5:
                raise ValidationError("Minimum Capacity is 5")
            
                

