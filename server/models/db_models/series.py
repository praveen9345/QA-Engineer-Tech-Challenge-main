from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from utils.database import Base


class SeriesDB(Base):
    __tablename__ = "series"

    series_instance_uid = Column(String, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    patient_name = Column(String, index=True)
    study_instance_uid = Column(String)
    instances_in_series = Column(Integer, default=0)
