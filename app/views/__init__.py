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
    odb,
    session,
)


def add_views(app: Flask):
    """ Adds all of the views to the application """
    auth.AuthViews.add_views(app)
    health.HealthViews.add_views(app)
    index.IndexViews.add_views(app)
    user.UserViews.add_views(app)

    # ODB
    odb.ODBViews.add_views(app)
    session.SessionViews.add_views(app)
