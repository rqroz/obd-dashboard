"""
Fuel Views.
"""
from flask import jsonify

from app.constants.odb import ODBSensorNames
from app.controllers.odb.fuel import FuelController
from app.decorators import auth_required
from app.views.odb import BaseSensorViews


class FuelViews(BaseSensorViews):
    CONTROLLER_CLASS = FuelController
    SENSORS = [
        ODBSensorNames.Fuel.LAMBDA,
        ODBSensorNames.Fuel.LEVEL,
        ODBSensorNames.Fuel.RATIO,
    ]
    VIEW_PREFIX = 'fuel'

    # --------------------------------------------- LAMBDA ---------------------------------------------------------- #
    @auth_required
    def lambda_avg_view(user):
        """ Retrieves the historical average coolant temperature for the current user """
        return FuelViews._get_avg(user, ODBSensorNames.Fuel.LAMBDA)

    @auth_required
    def lambda_latest_view(user):
        """ Retrieves the latest coolant temperature value for the current user """
        return FuelViews._get_latest(user, ODBSensorNames.Fuel.LAMBDA)

    # ---------------------------------------------- LEVEL ---------------------------------------------------------- #
    @auth_required
    def level_avg_view(user):
        """ Retrieves the historical average coolant temperature for the current user """
        return FuelViews._get_avg(user, ODBSensorNames.Fuel.LEVEL)

    @auth_required
    def level_latest_view(user):
        """ Retrieves the latest coolant temperature value for the current user """
        return FuelViews._get_latest(user, ODBSensorNames.Fuel.LEVEL)

    # ---------------------------------------------- RATIO ---------------------------------------------------------- #
    @auth_required
    def ratio_avg_view(user):
        """ Retrieves the historical average coolant temperature for the current user """
        return FuelViews._get_avg(user, ODBSensorNames.Fuel.RATIO)

    @auth_required
    def ratio_latest_view(user):
        """ Retrieves the latest coolant temperature value for the current user """
        return FuelViews._get_latest(user, ODBSensorNames.Fuel.RATIO)
