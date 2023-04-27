from datetime import datetime as dt

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.database import Base


class Reports(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False, default=dt.utcnow())
    temp = Column(Integer, nullable=False)
    feels_like = Column(Integer, nullable=False)
    wind_speed = Column(Integer, nullable=False)
    pressure_mm = Column(Integer, nullable=False)
    city = Column(String, nullable=False)

    def __repr__(self):
        return f"Report for {self.city}"
