"""
Session Views.
"""
from flask import jsonify

from app.controllers.obd.session import SessionController
from app.decorators import auth_required


class SessionViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule(
            '/api/sessions/',
            'session_list_view',
            view_func=cls.session_list_view,
            methods=('GET',),
        )
        server.add_url_rule(
            '/api/sessions/<string:session_id>/',
            'session_get_view',
            view_func=cls.session_get_view,
            methods=('GET',),
        )
        server.add_url_rule(
            '/api/sessions/summary/',
            'session_summary_view',
            view_func=cls.summary_view,
            methods=('GET',),
        )
        server.add_url_rule(
            '/api/sessions/locations/',
            'session_locations_view',
            view_func=cls.locations_view,
            methods=('GET',),
        )

    @auth_required
    def session_list_view(user):
        """ Retrieves basic data on all sessions for the current user """
        sessions = SessionController(user_id=user.id).get_all()
        return jsonify({'list': [session.to_dict() for session in sessions]})

    @auth_required
    def session_get_view(user, session_id):
        """ Retrieves complete data package on a certain session for the current user """
        session = SessionController(user_id=user.id).get(session_id)
        if not session:
            response = jsonify({'message': 'Unable to find session'})
            response.status_code = 404
            return response

        data = session.to_dict()
        data['car_states'] = [state.to_dict() for state in session.car_states]
        return jsonify(data)

    @auth_required
    def summary_view(user):
        return jsonify(SessionController(user_id=user.id).get_summary())

    @auth_required
    def locations_view(user):
        return jsonify(SessionController(user_id=user.id).get_locations())
