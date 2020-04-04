"""
User specific models.
"""
import uuid
import datetime

from sqlalchemy import (
    Binary,
    Column,
    DateTime,
    Integer,
    Sequence,
    String,
)

from app.database import DATABASE
from app.models import DictDataModel


class User(DATABASE.Model, DictDataModel):
    __tablename__ = "user"

    private_fields = ["password"]
    protected_fields = ["email", "first_name", "last_name"]

    id = Column(Integer, Sequence("user_id_seq", start=514433), primary_key=True)
    public_id = Column(String(36), unique=True)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    password = Column(Binary)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self, include_protected=False, replace_id=False):
        data = super(User, self).to_dict(include_protected)
        if replace_id:
            data['id'] = data.pop('public_id')
        return data
