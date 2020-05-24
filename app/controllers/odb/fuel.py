"""
Fuel Controller
"""
from app.constants.odb import ODBSensorNames
from app.controllers.odb import BaseODBSensorController
from app.models.odb.fuel import (
    FuelLevel,
    FuelRatio,
    FuelLambda,
)
from app.models.user import User


class FuelController(BaseODBSensorController):
    """
    Controller class for Engine-related data manipulations.
    """
    MODEL_MAP = {
        ODBSensorNames.Fuel.LAMBDA: FuelLambda,
        ODBSensorNames.Fuel.LEVEL: FuelLevel,
        ODBSensorNames.Fuel.RATIO: FuelRatio,
    }
