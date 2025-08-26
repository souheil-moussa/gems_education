from odoo import http
from odoo.http import request

class GemsPortalController(http.Controller):

    @http.route(['/my/sessions'], type='http', auth='user', website=True)
    def portal_my_sessions(self, **kw):
        """List all sessions for the logged-in user (teacher or student)"""
        user = request.env.user
        sessions = request.env['gems.session'].sudo().search([
            '|',
            ('teacher_id', '=', user.id),
            ('student_ids', 'in', user.id)
        ], order='start_date asc')
        
        return request.render('gems_education.gems_portal_templates_list', {
            'sessions': sessions
        })

    @http.route(['/my/sessions/<int:session_id>'], type='http', auth='user', website=True)
    def portal_session_form(self, session_id, **kw):
        """Display single session details"""
        session = request.env['gems.session'].sudo().browse(session_id)
        if not session.exists():
            return request.not_found()
        
        return request.render('gems_education.gems_portal_templates_form', {
            'session': session
        })
