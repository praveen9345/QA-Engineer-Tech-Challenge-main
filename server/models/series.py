from pydantic import BaseModel

class Series(BaseModel):
    series_instance_uid: str
    patient_id: str
    patient_name: str
    study_instance_uid: str
    instances_in_series: int

    class Config:
        orm_mode = True
