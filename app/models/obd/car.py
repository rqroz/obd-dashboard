"""
Car State Model Definitions.
"""
import datetime

from pandas import DataFrame
from structlog import get_logger

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship

from app.constants.obd import CSV_SENSOR_MAP, CarSensorID
from app.database import DATABASE
from app.models import DictDataModel
from app.models.obd.session import OBDSession


LOGGER = get_logger(__name__)


class Acceletometer(DATABASE.Model, DictDataModel):
    """ Acceletometer-specific model """
    __tablename__ = 'acceletometer_state'

    id = Column(Integer, primary_key=True)
    x = Column(Numeric, nullable=False)
    y = Column(Numeric, nullable=False)
    z = Column(Numeric, nullable=False)
    total = Column(Numeric, nullable=False)


class Engine(DATABASE.Model, DictDataModel):
    """ Engine-specific model """
    __tablename__ = 'engine_state'

    id = Column(Integer, primary_key=True)
    coolant_temp = Column(Numeric, nullable=False)
    load = Column(Numeric, nullable=False)
    intake_air_temp = Column(Numeric, nullable=False)
    maf = Column(Numeric, nullable=False)
    map = Column(Numeric, nullable=False)
    rpm = Column(Numeric, nullable=False)


class Fuel(DATABASE.Model, DictDataModel):
    """ Fuel-specific model """
    __tablename__ = 'fuel_state'

    id = Column(Integer, primary_key=True)
    cmd_equivalence_ratio = Column(Numeric, nullable=False)
    level = Column(Numeric, nullable=False)
    ratio = Column(Numeric, nullable=False)
    used = Column(Numeric, nullable=False)


class GPSReading(DATABASE.Model, DictDataModel):
    """ Readings for GPS data from OBD sensors. """
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
    session_id = Column(String, ForeignKey(OBDSession.id))
    acceletometer_id = Column(Integer, ForeignKey(Acceletometer.id))
    engine_id = Column(Integer, ForeignKey(Engine.id))
    fuel_id = Column(Integer, ForeignKey(Fuel.id))
    gps_id = Column(Integer, ForeignKey(GPSReading.id))

    speed = Column(Numeric, nullable=False)
    voltage = Column(Numeric, nullable=False)
    throttle_position = Column(Numeric, nullable=False)
    timestamp = Column(String(25), nullable=False)

    date = Column(DateTime, default=datetime.datetime.utcnow)

    acceletometer = relationship(Acceletometer, uselist=False)
    engine = relationship(Engine, uselist=False)
    fuel = relationship(Fuel, uselist=False)
    gps = relationship(GPSReading, uselist=False)
    session = relationship(OBDSession, uselist=False)

    def to_dict(self, include_protected=False):
        data = super(CarState, self).to_dict(include_protected)
        data.update({
            'acceletometer': self.acceletometer.to_dict(),
            'engine': self.engine.to_dict(),
            'fuel': self.fuel.to_dict(),
            'gps': self.gps.to_dict(),
        })
        data.pop('acceletometer_id')
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
            'throttle_position': self.throttle_position,
            'date': self.date,
            'timestamp': self.timestamp,
            'acceletometer_total': self.acceletometer.total,
            'acceletometer_x': self.acceletometer.x,
            'acceletometer_y': self.acceletometer.y,
            'acceletometer_z': self.acceletometer.z,
            'engine_coolant_temp': self.engine.coolant_temp,
            'engine_load': self.engine.load,
            'engine_intake_air_temp': self.engine.intake_air_temp,
            'engine_maf': self.engine.maf,
            'engine_map': self.engine.map,
            'engine_rpm': self.engine.rpm,
            'fuel_cmd_equivalence_ratio': self.fuel.cmd_equivalence_ratio,
            'fuel_level': self.fuel.level,
            'fuel_ratio': self.fuel.ratio,
            'fuel_used': self.fuel.used,
        }

    @classmethod
    def create_from_csv(cls, db_session, session: OBDSession, csv: DataFrame):
        """
        Creates a list of instances from a TORQUE generated CSV.

        Args:
            - session (app.models.obd.session.OBDSession): Current session to attach instance to;
            - csv (pandas.DataFrame): DataFrame representation of TORQUE generated CSV.

        Returns:
            - (List[cls]): List of created instances.
        """
        def row_value(row, key):
            value = row[CSV_SENSOR_MAP[key]]
            return value if value != '-' else 0

        car_states = []
        for _, row in csv.iterrows():
            try:
                acceletometer = Acceletometer(
                    total=row_value(row, CarSensorID.Accelerometer.TOTAL),
                    x=row_value(row, CarSensorID.Accelerometer.X),
                    y=row_value(row, CarSensorID.Accelerometer.Y),
                    z=row_value(row, CarSensorID.Accelerometer.Z),
                )
                db_session.add(acceletometer)

                fuel = Fuel(
                    cmd_equivalence_ratio=row_value(row, CarSensorID.Fuel.LAMBDA),
                    level=row_value(row, CarSensorID.Fuel.LEVEL),
                    ratio=row_value(row, CarSensorID.Fuel.RATIO),
                    used=row_value(row, CarSensorID.Fuel.USED),
                )
                db_session.add(fuel)

                engine = Engine(
                    coolant_temp=row_value(row, CarSensorID.Engine.COOLANT_TEMP),
                    load=row_value(row, CarSensorID.Engine.LOAD),
                    intake_air_temp=row_value(row, CarSensorID.Engine.INTAKE_AIR_TEMP),
                    maf=row_value(row, CarSensorID.Engine.MAF),
                    map=row_value(row, CarSensorID.Engine.MAP),
                    rpm=row_value(row, CarSensorID.Engine.RPM),
                )
                db_session.add(engine)

                gps = GPSReading(
                    lat=row_value(row, CarSensorID.GPS.LATITUDE),
                    lng=row_value(row, CarSensorID.GPS.LONGITUDE),
                )
                db_session.add(gps)

                db_session.flush()

                date_str = row_value(row, CarSensorID.DATE)
                date = datetime.datetime.strptime(date_str, '%d-%b-%Y %H:%M:%S.%f')
                curr_state = cls(
                    acceletometer_id=acceletometer.id,
                    engine_id=engine.id,
                    fuel_id=fuel.id,
                    gps_id=gps.id,
                    session_id=session.id,
                    date=date,
                    speed=row_value(row, CarSensorID.SPEED),
                    voltage=row_value(row, CarSensorID.VOLTAGE),
                    throttle_position=row_value(row, CarSensorID.THROTTLE_POSITION),
                    timestamp=str(date.timestamp()).replace('.', '')[:13],
                )
                db_session.add(curr_state)
                db_session.flush()
            except Exception as err:
                LOGGER.error('TORQUE: Could not save car state', error=str(err))
            else:
                car_states.append(curr_state)

        return car_states

    @classmethod
    def create_from_torque(cls, db_session, session: OBDSession, data: dict):
        """
        Creates an instance from TORQUE's request data.

        Args:
            - session (app.models.obd.session.OBDSession): Current session to attach instance to;
            - data (dict): Request data from TORQUE.
            - date (datetime.datetime): Date to attach to instance.

        Returns:
            - (cls | None): An instance of <cls>, if able to resolve sensor data from the request. Otherwise, None.
        """
        try:
            acceletometer = Acceletometer(
                total=data.get(CarSensorID.Accelerometer.TOTAL, 0),
                x=data.get(CarSensorID.Accelerometer.X, 0),
                y=data.get(CarSensorID.Accelerometer.Y, 0),
                z=data.get(CarSensorID.Accelerometer.Z, 0),
            )
            db_session.add(acceletometer)

            fuel = Fuel(
                cmd_equivalence_ratio=data.get(CarSensorID.Fuel.LAMBDA, 0),
                level=data.get(CarSensorID.Fuel.LEVEL, 0),
                ratio=data.get(CarSensorID.Fuel.RATIO, 0),
                used=data.get(CarSensorID.Fuel.USED, 0),
            )
            db_session.add(fuel)

            engine = Engine(
                coolant_temp=data.get(CarSensorID.Engine.COOLANT_TEMP, 0),
                load=data.get(CarSensorID.Engine.LOAD, 0),
                intake_air_temp=data.get(CarSensorID.Engine.INTAKE_AIR_TEMP, 0),
                maf=data.get(CarSensorID.Engine.MAF, 0),
                map=data.get(CarSensorID.Engine.MAP, 0),
                rpm=data.get(CarSensorID.Engine.RPM, 0),
            )
            db_session.add(engine)

            gps = GPSReading(
                lat=data.get(CarSensorID.GPS.LATITUDE, 0),
                lng=data.get(CarSensorID.GPS.LONGITUDE, 0),
            )
            db_session.add(gps)

            db_session.flush()

            car_state = cls(
                acceletometer_id=acceletometer.id,
                engine_id=engine.id,
                fuel_id=fuel.id,
                gps_id=gps.id,
                session_id=session.id,
                speed=data.get(CarSensorID.SPEED, 0),
                voltage=data.get(CarSensorID.VOLTAGE, 0),
                throttle_position = data.get(CarSensorID.THROTTLE_POSITION, 0),
                timestamp=data[CarSensorID.TIMESTAMP],
            )
            db_session.add(car_state)
            db_session.flush()
        except Exception as err:
            LOGGER.error('TORQUE: Could not save car state', error=str(err))
            return None

        return car_state
