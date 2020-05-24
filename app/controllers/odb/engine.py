"""
Engine Controller
"""
from sqlalchemy.sql import func

from app.constants.odb import ODBSensorNames
from app.controllers.odb import BaseODBSensorController
from app.models.odb.engine import (
    EngineLoad,
    EngineRPM,
    EngineCoolantTemp,
    EngineVoltage,
    ManifoldPressure,
    MassAirFlow,
    Speed,
)
from app.models.user import User


class EngineController(BaseODBSensorController):
    """
    Controller class for Engine-related data manipulations.
    """
    MODEL_MAP = {
        ODBSensorNames.Engine.COOLANT_TEMP: EngineCoolantTemp,
        ODBSensorNames.Engine.LOAD: EngineLoad,
        ODBSensorNames.Engine.MAF: MassAirFlow,
        ODBSensorNames.Engine.MAP: ManifoldPressure,
        ODBSensorNames.Engine.RPM: EngineRPM,
        ODBSensorNames.Engine.SPEED: Speed,
        ODBSensorNames.Engine.VOLTAGE: EngineVoltage,
    }
