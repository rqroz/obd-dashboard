"""
ODB Controller
"""
from sqlalchemy.sql import func

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
        'load': EngineLoad,
        'rmp': EngineRPM,
        'coolant_temp': EngineCoolantTemp,
        'battery': EngineVoltage,
        'map': ManifoldPressure,
        'maf': MassAirFlow,
        'speed': Speed,
    }

    def _get_average(self, engine_class: any, user: User):
        """
        Returns the average from the registered values for a certain Engine sensor,
        considering the complete history of a certain user.
        """
        return (
            self.db_session.query(func.avg(engine_class.value))
                            .filter(engine_class.session.has(user_id=user.id))
        ).scalar()

    def get_load_avg(self, user: User):
        """
        Returns the average engine load considering the complete history of a certain user.
        """
        return self._get_average(EngineLoad, user)

    def get_rpm_avg(self, user: User):
        """
        Returns the average engine RPM considering the complete history of a certain user.
        """
        return self._get_average(EngineRPM, user)

    def get_speed_avg(self, user: User):
        """
        Returns the average engine RPM considering the complete history of a certain user.
        """
        return self._get_average(Speed, user)

    def get_battery_latest_read(self, user: User):
        engine_voltage = (
            self.db_session.query(EngineVoltage.value)
                            .filter(EngineVoltage.session.has(user_id=user.id))
                            .order_by(EngineVoltage.date.desc())
                            .first()
        )
        return engine_voltage.value if engine_voltage else None
