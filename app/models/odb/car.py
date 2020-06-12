"""
Car State Model Definitions.
"""
import datetime

from pandas import DataFrame
from structlog import get_logger

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship

from app.constants.odb import CSV_SENSOR_MAP, CarSensorID
from app.database import DATABASE
from app.models import DictDataModel
from app.models.odb.session import ODBSession


LOGGER = get_logger(__name__)


class Engine(DATABASE.Model, DictDataModel):
    """ Engine-specific model """
    __tablename__ = 'engine_state'

    id = Column(Integer, primary_key=True)
    coolant_temp = Column(Numeric, nullable=False)
    load = Column(Numeric, nullable=False)
    maf = Column(Numeric, nullable=False)
    map = Column(Numeric, nullable=False)
    rpm = Column(Numeric, nullable=False)


class Fuel(DATABASE.Model, DictDataModel):
    """ Fuel-specific model """
    __tablename__ = 'fuel_state'

    id = Column(Integer, primary_key=True)
    level = Column(Numeric, nullable=False)
    ratio = Column(Numeric, nullable=False)
    cmd_equivalence_ratio = Column(Numeric, nullable=False)


class GPSReading(DATABASE.Model, DictDataModel):
    """ Readings for GPS data from ODB sensors. """
    __tablename__ = 'gps_location'

    id = Column(Integer, primary_key=True)
    lat = Column(Numeric, nullable=False)
    lng = Column(Numeric, nullable=False)

    def get_point(self):
        return {'lat': self.lat, 'lng': self.lng}


class CarState(DATABASE.Model, DictDataModel):
    """ Representation of the car measures from a certain point in time """
    __tablename__ = 'car_state'

    id = Column(Integer, primary_key=True)
    session_id = Column(String, ForeignKey(ODBSession.id))
    engine_id = Column(Integer, ForeignKey(Engine.id))
    fuel_id = Column(Integer, ForeignKey(Fuel.id))
    gps_id = Column(Integer, ForeignKey(GPSReading.id))

    speed = Column(Numeric, nullable=False)
    voltage = Column(Numeric, nullable=False)

    date = Column(DateTime, default=datetime.datetime.utcnow)

    engine = relationship(Engine, uselist=False)
    fuel = relationship(Fuel, uselist=False)
    gps = relationship(GPSReading, uselist=False)
    session = relationship(ODBSession, uselist=False)

    def to_dict(self, include_protected=False):
        data = super(CarState, self).to_dict(include_protected)
        data.update({
            'engine': self.engine.to_dict(),
            'fuel': self.fuel.to_dict(),
            'gps': self.gps.to_dict(),
        })
        data.pop('engine_id')
        data.pop('fuel_id')
        data.pop('gps_id')
        return data

    def to_flat_data(self):
        """ Flattens the data for the current state """
        return {
            'id': self.id,
            'speed': self.speed,
            'voltage': self.voltage,
            'date': self.date,
            'engine_coolant_temp': self.engine.coolant_temp,
            'engine_load': self.engine.load,
            'engine_maf': self.engine.maf,
            'engine_map': self.engine.map,
            'engine_rpm': self.engine.rpm,
            'fuel_level': self.fuel.level,
            'fuel_ratio': self.fuel.ratio,
            'fuel_cmd_equivalence_ratio': self.fuel.cmd_equivalence_ratio,
        }

    @classmethod
    def create_from_csv(cls, db_session, session: ODBSession, csv: DataFrame):
        """
        Creates a list of instances from a TORQUE generated CSV.

        Args:
            - session (app.models.odb.session.ODBSession): Current session to attach instance to;
            - csv (pandas.DataFrame): DataFrame representation of TORQUE generated CSV.

        Returns:
            - (List[cls]): List of created instances.
        """
        row_value = lambda row, key: row[CSV_SENSOR_MAP[key]]
        car_states = []
        for _, row in csv.iterrows():
            try:
                gps = GPSReading(
                    lat=row_value(row, CarSensorID.GPS.LATITUDE),
                    lng=row_value(row, CarSensorID.GPS.LONGITUDE),
                )
                db_session.add(gps)

                fuel = Fuel(
                    level=row_value(row, CarSensorID.Fuel.LEVEL),
                    ratio=row_value(row, CarSensorID.Fuel.RATIO),
                    cmd_equivalence_ratio=row_value(row, CarSensorID.Fuel.LAMBDA),
                )
                db_session.add(fuel)

                engine = Engine(
                    coolant_temp=row_value(row, CarSensorID.Engine.COOLANT_TEMP),
                    load=row_value(row, CarSensorID.Engine.LOAD),
                    maf=row_value(row, CarSensorID.Engine.MAF),
                    map=row_value(row, CarSensorID.Engine.MAP),
                    rpm=row_value(row, CarSensorID.Engine.RPM),
                )
                db_session.add(engine)

                db_session.flush()

                date_str = row_value(row, CarSensorID.DATE)
                curr_state = cls(
                    engine_id=engine.id,
                    fuel_id=fuel.id,
                    gps_id=gps.id,
                    session_id=session.id,
                    date=datetime.datetime.strptime(date_str, '%d-%b-%Y %H:%M:%S.%f'),
                    speed=row_value(row, CarSensorID.SPEED),
                    voltage=row_value(row, CarSensorID.VOLTAGE),
                )
                db_session.add(curr_state)
                db_session.flush()

                car_states.apppend(curr_state)
            except:
                continue

        return car_states

    @classmethod
    def create_from_torque(cls, session: ODBSession, request_data: dict, date: datetime.datetime):
        """
        Creates an instance from TORQUE's request data.

        Args:
            - session (app.models.odb.session.ODBSession): Current session to attach instance to;
            - request_data (dict): Request data from TORQUE.
            - date (datetime.datetime): Date to attach to instance.

        Returns:
            - (cls | None): An instance of <cls>, if able to resolve sensor data from the request. Otherwise, None.
        """
        if cls.SENSOR_KEY not in request_data:
            return None
        else:
            value = request_data[cls.SENSOR_KEY]
            LOGGER.info(f'Will create instance of {cls.__name__}', value=value)
            return cls(session_id=session.id, value=value, date=date)
