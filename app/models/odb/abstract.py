"""
Abstract models.
"""
import datetime

from pandas import DataFrame
from structlog import get_logger

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from app.constants.odb import CSV_COLUM_SENSOR_MAP, ODBSensorLabels
from app.database import DATABASE
from app.models import DictDataModel
from app.models.odb.session import ODBSession
from app.models.user import User


LOGGER = get_logger(__name__)


class ODBSensorMixin(DictDataModel):
    """ Base absctract class for ODB Sensors """
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    DATE_KEY = ODBSensorLabels.DATE

    @declared_attr
    def session_id(cls):
        return Column(String, ForeignKey(ODBSession.id))

    @declared_attr
    def session(cls):
        return relationship(ODBSession, uselist=False)

    @classmethod
    def resolve_date_from_csv_row(cls, csv_row: dict):
        """ Resolves a datetime from a certain row in a TORQUE generated CSV """
        date_str = csv_row[CSV_COLUM_SENSOR_MAP[cls.DATE_KEY]]
        return datetime.datetime.strptime(date_str[:-4], '%d-%b-%Y %H:%M:%S')


class ODBSensorValueMixin(ODBSensorMixin):
    """ Base absctract class for ODB Sensors """
    value = Column(Numeric, nullable=False)

    SENSOR_KEY = None

    @classmethod
    def create_from_csv(cls, session: ODBSession, csv: DataFrame):
        """
        Creates a list of instances from a TORQUE generated CSV.

        Args:
            - session (app.models.odb.session.ODBSession): Current session to attach instance to;
            - csv (pandas.DataFrame): DataFrame representation of TORQUE generated CSV.

        Returns:
            - (List[cls]): List of created instances.
        """
        csv_key = CSV_COLUM_SENSOR_MAP[cls.SENSOR_KEY]

        items = []
        for idx, row in csv.iterrows():
            try:
                item = cls(
                    session_id=session.id,
                    value=row[csv_key],
                    date=cls.resolve_date_from_csv_row(row),
                )
            except:
                continue

            items.append(item)

        return items

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
