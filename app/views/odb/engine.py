"""
Engine Views.
"""
from flask import jsonify

from app.constants.odb import BatteryLevel, ODBSensorNames
from app.controllers.odb.engine import EngineController
from app.decorators import auth_required
from app.views.odb import BaseSensorViews


class EngineViews(BaseSensorViews):
    CONTROLLER_CLASS = EngineController
    SENSORS = [
        ODBSensorNames.Engine.COOLANT_TEMP,
        ODBSensorNames.Engine.LOAD,
        ODBSensorNames.Engine.MAF,
        ODBSensorNames.Engine.MAP,
        ODBSensorNames.Engine.RPM,
        ODBSensorNames.Engine.SPEED,
        ODBSensorNames.Engine.VOLTAGE,
    ]
    VIEW_PREFIX = 'engine'

    # -------------------------------------------- COOLANT ---------------------------------------------------------- #
    @auth_required
    def coolant_avg_view(user):
        """ Retrieves the historical average coolant temperature for the current user """
        return EngineViews._get_avg(user, ODBSensorNames.Engine.COOLANT_TEMP)

    @auth_required
    def coolant_latest_view(user):
        """ Retrieves the latest coolant temperature value for the current user """
        return EngineViews._get_latest(user, ODBSensorNames.Engine.COOLANT_TEMP)

    # ------------------------------------------- ENGINE LOAD ------------------------------------------------------- #
    @auth_required
    def load_avg_view(user):
        """ Retrieves the historical average engine load for the current user """
        return EngineViews._get_avg(user, ODBSensorNames.Engine.LOAD)

    @auth_required
    def load_latest_view(user):
        """ Retrieves the latest engine load value for the current user """
        return EngineViews._get_latest(user, ODBSensorNames.Engine.LOAD)

    # ----------------------------------------------- MAF ----------------------------------------------------------- #
    @auth_required
    def maf_avg_view(user):
        """ Retrieves the historical average MAF for the current user """
        return EngineViews._get_avg(user, ODBSensorNames.Engine.MAF)

    @auth_required
    def maf_latest_view(user):
        """ Retrieves the latest MAF value for the current user """
        return EngineViews._get_latest(user, ODBSensorNames.Engine.MAF)

    # ----------------------------------------------- MAP ----------------------------------------------------------- #
    @auth_required
    def map_avg_view(user):
        """ Retrieves the historical average MAP for the current user """
        return EngineViews._get_avg(user, ODBSensorNames.Engine.MAP)

    @auth_required
    def map_latest_view(user):
        """ Retrieves the latest MAP value for the current user """
        return EngineViews._get_latest(user, ODBSensorNames.Engine.MAP)

    # ----------------------------------------------- RPM ----------------------------------------------------------- #
    @auth_required
    def rpm_avg_view(user):
        """ Retrieves the historical average rpm for the current user """
        return EngineViews._get_avg(user, ODBSensorNames.Engine.RPM)

    @auth_required
    def rpm_latest_view(user):
        """ Retrieves the latest RPM value for the current user """
        return EngineViews._get_latest(user, ODBSensorNames.Engine.RPM)

    # --------------------------------------------- SPEED ----------------------------------------------------------- #
    @auth_required
    def speed_avg_view(user):
        """ Retrieves the historical average speed for the current user """
        return EngineViews._get_avg(user, ODBSensorNames.Engine.SPEED)

    @auth_required
    def speed_latest_view(user):
        """ Retrieves the latest speed value for the current user """
        return EngineViews._get_latest(user, ODBSensorNames.Engine.SPEED)

    # ------------------------------------------- BATTERY ----------------------------------------------------------- #
    @auth_required
    def battery_avg_view(user):
        """ Retrieves the historical average battery voltage for the current user """
        return EngineViews._get_avg(user, ODBSensorNames.Engine.VOLTAGE)

    @auth_required
    def battery_latest_view(user):
        """ Retrieves the latest battery read for the current user """
        return jsonify({
            'value': EngineController().get_sensor_latest_value(user, ODBSensorNames.Engine.VOLTAGE),
            'min_healthy': BatteryLevel.MIN,
        })
