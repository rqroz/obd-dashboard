"""
All of the views
"""
from flask import Flask

from app.views import (
    auth,
    index,
    health,
    user,
)
from app.views.odb import (
    engine,
    fuel,
    gps,
    odb,
)


def add_views(app: Flask):
    """ Adds all of the views to the application """
    auth.AuthViews.add_views(app)
    health.HealthViews.add_views(app)
    index.IndexViews.add_views(app)
    user.UserViews.add_views(app)

    # ODB
    engine.EngineViews.add_views(app)
    fuel.FuelViews.add_views(app)
    gps.GPSViews.add_views(app)
    odb.ODBViews.add_views(app)
