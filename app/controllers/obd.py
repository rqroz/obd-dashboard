"""
OBD Controller
"""
import datetime
import pandas
import re

from io import StringIO
from typing import List
from structlog import get_logger
from sqlalchemy.orm import selectinload

from app.constants.obd import (
    OBDSensorPrefixes,
    OBDSensorLabels,
    CSV_COLUM_SENSOR_MAP,
)
from app.controllers import BaseController
from app.models.obd import (
    OBDSensorUnit,
    OBDSensor,
    OBDSensorUser,
    OBDSensorValue,
)
from app.models.odb import ODBSession
from app.models.odb.gps import GPSReading
from app.models.user import User


LOGGER = get_logger(__name__)


class OBDControllerError(Exception):
    """ Exception class for OBD Controller """
    pass


class OBDController(BaseController):
    """
    Controller class for OBD-related data manipulations.

    Attributes:
        - PREFIXES (app.constants.obd.OBDSensorPrefixes): Set of prefixes used to extract data from TORQUE request.
    """
    PREFIXES = OBDSensorPrefixes

    def _resolve_user(self, data: dict):
        """
        Resolves user from data.

        Raises:
            - OBDControllerError:
                If user email is not found in <data>;
                If there is no user corresponding to the email found in <data>;

        Args:
            - data (dict): Map of arguments received by TORQUE request.

        Returns:
            - user (app.models.user.User): User instance.
        """
        user_email = data.get('eml')
        if not user_email:
            raise OBDControllerError('User email not found')

        user: User = self.db_session.query(User).filter(User.email == user_email).first()
        if not user:
            raise OBDControllerError('User does not exist')

        return user

    def _get_unit(self, label: str):
        """
        OBDSensorUnit: Get method.
        Will fetch the first item matching label.

        Args:
            - label (str): Label identifying record.

        Returns:
            (app.models.obd.OBDSensorUnit | None): First item matching label, if any. None otherwise.
        """
        return self.db_session.query(OBDSensorUnit).filter(OBDSensorUnit.label == label).first()

    def _get_sensor(self, label: str):
        """
        OBDSensor: Get method.
        Will fetch the first item matching label.

        Args:
            - label (str): Label identifying record.

        Returns:
            (app.models.obd.OBDSensor | None): First item matching label, if any. None otherwise.
        """
        return self.db_session.query(OBDSensor).filter(OBDSensor.label == label).first()

    def _get_sensor_user(self, **kwargs):
        """
        OBDSensorUser: Get method.
        Will fetch the first item matching keyword arguments informed.

        Returns:
            (app.models.obd.OBDSensorUser | None): First item matching kwargs, if any. None otherwise.
        """
        return (
            self.db_session.query(OBDSensorUser)
                            .filter(*[getattr(OBDSensorUser, key) == value for key, value in kwargs.items()])
                            .first()
        )

    def _get_sensor_user_by_label(self, user: User, label: str):
        """
        Will get a OBDSensorUser object based on the informed user and sensor label.

        Args:
            - user (app.models.user.User): A user instance;
            - label (str): Sensor label;

        Returns:
            - (app.models.obd.OBDSensorUser | None): An instance of OBDSensorUser, if it exists. Otherwise None.
        """
        return (
            self.db_session.query(OBDSensorUser)
                            .filter(
                                OBDSensorUser.user_id == user.id,
                                OBDSensorUser.sensor.has(label=label),
                            )
                            .first()
        )

    def _get_or_create_sensor(self, label: str, full_name: str, short_name: str):
        """
        OBDSensor: Get or Create method.
        Will try to resolve an OBDSensor instance by a match with the label informed.
        If no record is found, will create one, add to the DB and perform a flush.

        Args:
            - label (str): Label of the sensor;
            - full_name (str): Full, detailed name of the sensor;
            - short_name (str): Short, simplified name of the sensor.

        Returns:
            - unit (app.models.obd.OBDSensorUnit): Resolved instance of OBDSensorUnit.
        """
        sensor: OBDSensor = self._get_sensor(label)
        if not sensor:
            sensor = OBDSensor(label=label, full_name=full_name, short_name=short_name)
            self.db_session.add(sensor)
            self.db_session.flush()

        return sensor

    def _get_or_create_unit(self, label: str):
        """
        OBDSensorUnit: Get or Create method.
        Will try to resolve an OBDSensorUnit instance by a match with the label informed.
        If no record is found, will create one, add to the DB and perform a flush.

        Args:
            - label (str): Label of the unit.

        Returns:
            - unit (app.models.obd.OBDSensorUnit): Resolved instance of OBDSensorUnit.
        """
        unit: OBDSensorUnit = self._get_unit(label)
        if not unit:
            unit = OBDSensorUnit(label=label)
            self.db_session.add(unit)
            self.db_session.flush()

        return unit

    def _get_or_create_sensor_user(self, user: User, sensor: OBDSensor, unit: OBDSensorUnit):
        """
        OBDSensorUser: Get or Create method.
        Will try to resolve an OBDSensorUser instance by a match with all of the arguments.
        If no record is found, will create one, add to the DB and perform a flush.

        Args:
            - user (app.models.user.User): User instance;
            - sensor (app.models.obd.OBDSensor): OBDSensor instance;
            - unit (app.models.obd.OBDSensorUnit): OBDSensorUnit instance.

        Returns:
            - obd_sensor_user (app.models.obd.OBDSensorUser): Resolved instance of OBDSensorUser.
        """
        obd_sensor_user: OBDSensorUser = self._get_sensor_user(user_id=user.id, sensor_id=sensor.id, unit_id=unit.id)
        if not obd_sensor_user:
            obd_sensor_user = OBDSensorUser(user_id=user.id, sensor_id=sensor.id, unit_id=unit.id)
            self.db_session.add(obd_sensor_user)
            self.db_session.flush()

        return obd_sensor_user

    def _register_sensor_list(self, labels: List[str], data: dict):
        """
        Will loop through the list of labels for the sensors and create the corresponding records in the database.
        Recovers the result OBDSensorUser object for each label and log its data as INFO.

        Args:
            - labels (List[str]): List of labels identifying the sensors;
            - data (dict): Supporting data containing information such as long name, short name, and unit
                           for each of the sensors specified by <labels>.
        """
        user = self._resolve_user(data)
        for label in labels:
            sensor = self._get_or_create_sensor(
                label,
                data.get(f'{self.PREFIXES.FULL_NAME}{label}'),
                data.get(f'{self.PREFIXES.SHORT_NAME}{label}'),
            )
            unit = self._get_or_create_unit(data.get(f'{self.PREFIXES.UNIT}{label}'))
            obd_sensor_user = self._get_or_create_sensor_user(user, sensor, unit)
            LOGGER.info('Resolved OBDSensorUser', **obd_sensor_user.to_dict())

        self.db_session.commit()

    def _register_sensor_values(self, data: dict):
        """
        Will loop through the list of sensor values resolved from <data> and register a OBDSensorValue record for
        any sensor that is attached to the user (also specified in <data>).

        Args:
            - data (dict): Map of values originated from TORQUE request.
        """
        user = self._resolve_user(data)
        session_id = data.get('session')
        if not session_id:
            raise OBDControllerError('Session is not specified')

        sensor_keys = list(filter(re.compile(f'{self.PREFIXES.SENSOR}.*').match, data.keys()))
        for sensor_key in sensor_keys:
            sensor_label = sensor_key.replace(self.PREFIXES.SENSOR, '')
            sensor = self._get_sensor(sensor_label)
            if not sensor:
                # If current sensor does not exist, skip it
                continue

            sensor_user = self._get_sensor_user(user_id=user.id, sensor_id=sensor.id)
            if not sensor_user:
                # If current sensor is not attached to the user, skip it
                continue

            obd_sensor_value = OBDSensorValue(
                sensor_user_id=sensor_user.id,
                session_id=session_id,
                value=data[sensor_key],
            )
            LOGGER.info(
                'Registering value to sensor',
                user=user.id,
                name=sensor.full_name,
                sensor=sensor.label,
                value=obd_sensor_value.value,
                session=session_id,
            )
            self.db_session.add(obd_sensor_value)

        self.db_session.commit()

    def process_sensor_params(self, data: dict):
        """
        Process data receive from TORQUE.
        If identifies that the data is composed by keys identifying sensor specs, will register such specs in the DB.
        Otherwise will look for values to link to the sensors and register in DB.

        Args:
            - data (dict): Data to be processed.
        """
        full_name_keys = list(filter(re.compile(f'{self.PREFIXES.FULL_NAME}.*').match, data.keys()))
        if full_name_keys:
            # Register Params
            labels = [full_name_key.replace(self.PREFIXES.FULL_NAME, '') for full_name_key in full_name_keys]
            self._register_sensor_list(labels, data)
        else:
            # Register Values
            self._register_sensor_values(data)

    def get_sensor_readings(self, user, label):
        """
        Returns a map of sensor readings, organized by session_id.
        Will query based on the user and label informed.

        TODO: Enhance query.

        Args:
            - user (app.models.user.User): User instance to retrieve id;
            - label (str): Label of the desired sensor to get the readings from.

        Returns:
            - (dict): Map of session_id => values.
        """
        sensor_user =  self._get_sensor_user_by_label(user, label)
        if not sensor_user:
            return {}

        sensor_values = (
            self.db_session.query(OBDSensorValue)
                            .filter(OBDSensorValue.sensor_user_id == sensor_user.id)
                            .all()
        )

        readings = {}
        for reading in sensor_values:
            if reading.session_id not in readings:
                readings[reading.session_id] = []
            readings[reading.session_id].append(reading.value)

        return readings

    def get_gps_readings(self, user: User):
        """
        Returns a list of GPS readings organized by session.

        Args:
            - user (app.models.user.User): User instance to be used when retrieving the sensor readings.

        Returns:
            (List[dict]): List of GPS points organized by session.
        """
        db_data = (
            self.db_session.query(ODBSession)
                            .filter(ODBSession.user_id == User.id)
                            .options(selectinload('gps_readings'))
        )

        readings = []
        for row in db_data:
            readings.append({
                'session_id': row.id,
                'date': row.date,
                'points': [gps.get_point() for gps in row.gps_readings]
            })

        return readings

    def register_gps_from_csv(self, session: ODBSession, csv: pandas.DataFrame):
        """
        Will read gps data from a CSV and register the values for the current user.
        """
        values = csv[CSV_COLUM_SENSOR_MAP.values()]
        for idx, row in values.iterrows():
            date_str = row[CSV_COLUM_SENSOR_MAP[OBDSensorLabels.DATE]]
            try:
                reading = GPSReading(
                    session_id=session.id,
                    lat=row[CSV_COLUM_SENSOR_MAP[OBDSensorLabels.GPS.LATITUDE]],
                    lng=row[CSV_COLUM_SENSOR_MAP[OBDSensorLabels.GPS.LONGITUDE]],
                    date=datetime.datetime.strptime(date_str[:-4], '%d-%b-%Y %H:%M:%S')
                )
            except:
                continue

            self.db_session.add(reading)

        self.db_session.flush()

    def process_csv(self, user: User, csv_file):
        """
        Will process a CSV file generated by the TORQUE application, registering the values for each
        considered sensor in the database.

        Args:
            - user (app.models.user.User): User instance;
            - csv_file (werkzeug.FileStorage): A file representation of the CSV file created by TORQUE.
        """
        csv = pandas.read_csv(StringIO(csv_file.read().decode('utf-8')), usecols=CSV_COLUM_SENSOR_MAP.values())
        session = ODBSession(id=str(datetime.datetime.now().timestamp()).replace('.', '')[:12], user_id=user.id)
        self.db_session.add(session)
        self.db_session.flush()
        self.register_gps_from_csv(session, csv)
        self.db_session.commit()
