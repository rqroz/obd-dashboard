import re

from structlog import get_logger
from flask import g

from app.constants.obd import OBDSensorPrefixes
from app.models.obd import (
    OBDSensorUnit,
    OBDSensor,
    OBDSensorUser,
    OBDSensorValue,
)
from app.models.user import User


LOGGER = get_logger(__name__)


class OBDControllerError(Exception):
    """ Exception class for OBD Controller """
    pass


class OBDController:
    """
    Controller class for OBD-related data manipulations.

    Attributes:
        - PREFIXES (app.constants.obd.OBDSensorPrefixes): Set of prefixes used to extract data from TORQUE request.
        - db_session (flask_sqlalchemy.SQLAlchemy.session): Database session instance.
    """
    PREFIXES = OBDSensorPrefixes

    def __init__(self, db_session=None):
        if db_session is None:
            db_session = g.db_session
        self.db_session = db_session

    def get_or_create_sensor(self, label: str, full_name: str, short_name: str):
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
        sensor: OBDSensor = self.db_session.query(OBDSensor).filter(OBDSensor.label == label).first()
        if not sensor:
            sensor = OBDSensor(label=label, full_name=full_name, short_name=short_name)
            self.db_session.add(sensor)
            self.db_session.flush()

        return sensor

    def get_or_create_unit(self, label: str):
        """
        OBDSensorUnit: Get or Create method.
        Will try to resolve an OBDSensorUnit instance by a match with the label informed.
        If no record is found, will create one, add to the DB and perform a flush.

        Args:
            - label (str): Label of the unit.

        Returns:
            - unit (app.models.obd.OBDSensorUnit): Resolved instance of OBDSensorUnit.
        """
        unit: OBDSensorUnit = self.db_session.query(OBDSensorUnit).filter(OBDSensorUnit.label == label).first()
        if not unit:
            unit = OBDSensorUnit(label=label)
            self.db_session.add(unit)
            self.db_session.flush()

        return unit

    def get_or_create_sensor_user(self, user: User, sensor: OBDSensor, unit: OBDSensorUnit):
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
        obd_sensor_user: OBDSensorUser = (
            self.db_session.query(OBDSensorUser)
                            .filter(
                                OBDSensorUser.user_id == user.id,
                                OBDSensorUser.sensor_id == sensor.id,
                                OBDSensorUser.unit_id == unit.id,
                            )
                            .first()
        )
        if not obd_sensor_user:
            obd_sensor_user = OBDSensorUser(user_id=user.id, sensor_id=sensor.id, unit_id=unit.id)
            self.db_session.add(obd_sensor_user)
            self.db_session.flush()

        return obd_sensor_user

    def register_sensor_list(self, labels, data):
        """
        Will loop through the list of labels for the sensors and create the corresponding records in the database.
        Recovers the result OBDSensorUser object for each label and log its data as INFO.

        Raises:
            - OBDControllerError:
                If user email is not found in <data>;
                If there is no user corresponding to the email found in <data>;

        Args:
            - labels ([str]): List of labels identifying the sensors;
            - data (dict): Supporting data containing information such as long name, short name, and unit
                           for each of the sensors specified by <labels>.
        """
        user_email = data.get('eml')
        if not user_email:
            raise OBDControllerError('User email not found')

        user: User = self.db_session.query(User).filter(User.email == user_email).first()
        if not user:
            raise OBDControllerError('User does not exist')

        for label in labels:
            sensor = self.get_or_create_sensor(
                label,
                data.get(f'{self.PREFIXES.FULL_NAME}{label}'),
                data.get(f'{self.PREFIXES.SHORT_NAME}{label}'),
            )
            unit = self.get_or_create_unit(data.get(f'{self.PREFIXES.UNIT}{label}'))
            obd_sensor_user = self.get_or_create_sensor_user(user, sensor, unit)
            LOGGER.info('Resolved OBDSensorUser', **obd_sensor_user.to_dict())

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
            self.register_sensor_list(labels, data)
        else:
            # Register Values
            pass
