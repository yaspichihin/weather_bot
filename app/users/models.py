from datetime import datetime as dt

from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.reports.models import Reports  # noqa


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    city = Column(String, nullable=True)
    connection_date = Column(DateTime, nullable=False, default=dt.utcnow())

    weather_reports = relationship(
        'Reports', backref='report', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"Telegram_id: {self.tg_id}"
