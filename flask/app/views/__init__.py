"""
All of the views
"""
from flask import Flask

import app.views.health as health
import app.views.obd as obd


def add_views(app: Flask):
    """ Adds all of the views to the application """
    obd.OBDViews.add_views(app)
    health.HealthViews.add_views(app)
