"""
App initializer
"""
from flask import jsonify


class AuthViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule('/api/login/', view_func=cls.login_view, methods=('POST',))
        server.add_url_rule('/api/logout/', view_func=cls.logout_view, methods=('POST',))
        server.add_url_rule('/api/register/', view_func=cls.registration_view, methods=('POST',))

    def login_view():
        user = {}
        return jsonify({'message': 'Login successful', 'user': user})

    def logout_view():
        return jsonify({'message': 'Successfully logged out'})

    def registration_view():
        user = {}
        return jsonify({'message': 'Registration successful', 'user': user})
