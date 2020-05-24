"""
Abstract models.
"""
import datetime

from pandas import DataFrame

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from app.constants.odb import CSV_COLUM_SENSOR_MAP, ODBSensorLabels
from app.database import DATABASE
from app.models import DictDataModel
from app.models.odb.session import ODBSession
from app.models.user import User


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
        Will read and store data related to the engine load from CSV for the current user.
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
