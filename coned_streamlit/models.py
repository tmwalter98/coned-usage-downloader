from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP, TEXT, DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class OpowerReadings(Base):
    __tablename__ = 'opower_readings'

    start_time = Column(TIMESTAMP(timezone=True), primary_key=True)
    end_time = Column(TIMESTAMP(timezone=True), primary_key=True)
    consumption_type = Column(TEXT)
    consumption_value = Column(DOUBLE_PRECISION)
