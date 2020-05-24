"""
ODB Controller
"""
import datetime

from decimal import Decimal
from pandas import DataFrame
from sqlalchemy.sql import func

from app.constants.odb import (
    ODBSensorLabels,
    CSV_COLUM_SENSOR_MAP,
)
from app.controllers.odb import BaseODBSensorController
from app.models.odb.session import ODBSession
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
    def register_coolant_temp_from_csv(self, session: ODBSession, csv: DataFrame, flush: bool = False):
        """
        Will read and store data related to the engine coolant temperature from CSV for the current user.
        """
        value_key = CSV_COLUM_SENSOR_MAP[ODBSensorLabels.Engine.COOLANT_TEMP]
        self._register_values_csv(EngineCoolantTemp, value_key, session, csv, flush)

    def register_load_from_csv(self, session: ODBSession, csv: DataFrame, flush: bool = False):
        """
        Will read and store data related to the engine load from CSV for the current user.
        """
        value_key = CSV_COLUM_SENSOR_MAP[ODBSensorLabels.Engine.LOAD]
        self._register_values_csv(EngineLoad, value_key, session, csv, flush)

    def register_voltage_from_csv(self, session: ODBSession, csv: DataFrame, flush: bool = False):
        """
        Will read and store data related to the engine voltage from CSV for the current user.
        """
        value_key = CSV_COLUM_SENSOR_MAP[ODBSensorLabels.Engine.VOLTAGE]
        self._register_values_csv(EngineVoltage, value_key, session, csv, flush)

    def register_map_from_csv(self, session: ODBSession, csv: DataFrame, flush: bool = False):
        """
        Will read and store data related to the engine MAP from CSV for the current user.
        """
        value_key = CSV_COLUM_SENSOR_MAP[ODBSensorLabels.Engine.MAP]
        self._register_values_csv(ManifoldPressure, value_key, session, csv, flush)

    def register_maf_from_csv(self, session: ODBSession, csv: DataFrame, flush: bool = False):
        """
        Will read and store data related to the engine MAF from CSV for the current user.
        """
        value_key = CSV_COLUM_SENSOR_MAP[ODBSensorLabels.Engine.MAF]
        self._register_values_csv(MassAirFlow, value_key, session, csv, flush)

    def register_rpm_from_csv(self, session: ODBSession, csv: DataFrame, flush: bool = False):
        """
        Will read and store data related to the engine load from CSV for the current user.
        """
        value_key = CSV_COLUM_SENSOR_MAP[ODBSensorLabels.Engine.RPM]
        self._register_values_csv(EngineRPM, value_key, session, csv, flush)

    def register_speed_from_csv(self, session: ODBSession, csv: DataFrame, flush: bool = False):
        """
        Will read and store data related to car speed from CSV for the current user.
        """
        value_key = CSV_COLUM_SENSOR_MAP[ODBSensorLabels.Engine.SPEED]
        self._register_values_csv(Speed, value_key, session, csv, flush)

    def register_coolant_temp(self, session: ODBSession, value: Decimal, date: datetime.datetime):
        """
        Will save an EngineCoolantTemp record on the database.
        """
        return self._register_value(EngineCoolantTemp, session, value, date)

    def register_load(self, session: ODBSession, value: Decimal, date: datetime.datetime):
        """
        Will save an EngineLoad record on the database.
        """
        return self._register_value(EngineLoad, session, value, date)

    def register_maf(self, session: ODBSession, value: Decimal, date: datetime.datetime):
        """
        Will save an MassAirFlow record on the database.
        """
        return self._register_value(MassAirFlow, session, value, date)

    def register_map(self, session: ODBSession, value: Decimal, date: datetime.datetime):
        """
        Will save an ManifoldPressure record on the database.
        """
        return self._register_value(ManifoldPressure, session, value, date)

    def register_rpm(self, session: ODBSession, value: Decimal, date: datetime.datetime):
        """
        Will save an EngineRPM record on the database.
        """
        return self._register_value(EngineRPM, session, value, date)

    def register_voltage(self, session: ODBSession, value: Decimal, date: datetime.datetime):
        """
        Will save an EngineVoltage record on the database.
        """
        return self._register_value(EngineVoltage, session, value, date)

    def register_speed(self, session: ODBSession, value: Decimal, date: datetime.datetime):
        """
        Will save an Speed record on the database.
        """
        return self._register_value(Speed, session, value, date)

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

    def get_battery_latest_read(self, user: User):
        engine_voltage = (
            self.db_session.query(EngineVoltage.value)
                            .filter(EngineVoltage.session.has(user_id=user.id))
                            .order_by(EngineVoltage.date.desc())
                            .first()
        )
        return engine_voltage.value if engine_voltage else None
