"""
Health check views for integration management
"""
import os
import datetime

from flask import Flask, jsonify


class HealthViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule("/health", "health_check_view", view_func=cls.health_check_view, methods=("GET",))

    def health_check_view():
        return jsonify({
            "status": "ok",
            "container": os.getenv("HOSTNAME"),
            "timestamp": datetime.datetime.now().timestamp()
        })
