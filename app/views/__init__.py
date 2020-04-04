"""
All of the views
"""
from flask import Flask

import app.views.auth as auth
import app.views.index as index
import app.views.health as health
import app.views.obd as obd


def add_views(app: Flask):
    """ Adds all of the views to the application """
    auth.AuthViews.add_views(app)
    health.HealthViews.add_views(app)
    index.IndexViews.add_views(app)
    obd.OBDViews.add_views(app)
