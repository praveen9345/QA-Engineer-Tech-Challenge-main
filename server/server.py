from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List
from models.series import Series
from models.db_models.series import SeriesDB
from utils import database

app = FastAPI()

@app.on_event("startup")
async def startup():
    database.create_tables()

@app.get("/")
async def root():
    """ A path to perform a basic health check of the server
    """
    return {"message": "Server is up!"}


@app.get("/all")
async def get_all_series(db: Session = Depends(database.get_db)) -> List[Series]:
    """ Returns all Series objects.
    """
    return db.query(SeriesDB).all()


@app.post("/add_series")
async def add_series(series_in: Series, db: Session = Depends(database.get_db)) -> str:
    series_in_data = jsonable_encoder(series_in)
    series_db = SeriesDB(**series_in_data)

    # Check for existing series and delete it
    existing_series = db.query(SeriesDB)\
        .filter(SeriesDB.series_instance_uid == series_in.series_instance_uid)\
        .first()
    if existing_series:
        db.delete(existing_series)

    db.add(series_db)
    db.commit()
    return "success"
