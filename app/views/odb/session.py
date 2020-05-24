"""
Session Views.
"""
from flask import jsonify

from app.controllers.odb.session import SessionController
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
            '/api/sessions/<int:session_id>/',
            'session_get_view',
            view_func=cls.session_get_view,
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
        data['readings'] = {
            'engine': {
                'load': [load.to_dict() for load in session.engine_load_readings],
                'rpm': [rpm.to_dict() for rpm in session.engine_rpm_readings],
                'maf': [maf.to_dict() for maf in session.engine_maf_readings],
                'map': [map.to_dict() for map in session.engine_map_readings],
                'coolant_temperature': [
                    coolant_temp.to_dict()
                    for coolant_temp
                    in session.engine_coolant_temp_readings
                ],
            },
            'battery': [battery.to_dict() for battery in session.engine_voltage_readings],
            'speed': [speed.to_dict() for speed in session.speed_readings],
            'fuel': {
                'level': [level.to_dict() for level in session.fuel_level_readings],
                'ratio': [ratio.to_dict() for ratio in session.fuel_ratio_readings],
                'lambda': [lbd.to_dict() for lbd in session.fuel_lambda_readings],
            },
            'gps': [gps.to_dict() for gps in session.gps_readings],
        }
        return jsonify(data)
