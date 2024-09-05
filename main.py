import time

import psycopg2
from fastapi import FastAPI, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor

import models
import schemas
from database import Session, get_db

app = FastAPI()
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='SIH', user='postgres', password='hellothere',
                                cursor_factory=RealDictCursor)

        cur = conn.cursor()
        print("Database Connection Successful!")
        break

    except Exception as error:
        print("Database connection failed")
        print("Error : ", error)
        time.sleep(2)


@app.get("/devices")
def read_root(db: Session = Depends(get_db)):
    data = db.query(models.Devices).all()
    return data


@app.get("/connections")
def read_root(db: Session = Depends(get_db)):
    data = db.query(models.Connections).all()
    return data


@app.get("/status")
def read_root(db: Session = Depends(get_db)):
    data = db.query(models.Status).all()
    return data


@app.get("/devices/{Id}")
def device_selected(Id: int, db: Session = Depends(get_db)):
    device = db.query(models.Devices).filter(models.Devices.id == Id).first()

    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {Id} not found")


@app.post("/new_device", response_model=schemas.Devices)
def add_device(post: schemas.Devices, db: Session = Depends(get_db)):
    new_post = models.Devices(**post.dict())  # ** unpacks the dict
    # It automatically takes the fields as a dict and then unpacks it to get the necessary result
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.post("/new_connection", response_model=schemas.Connections)
def add_connection(post: schemas.Connections, db: Session = Depends(get_db)):
    data = models.Connections(**post.dict())  # ** unpacks the dict
    # It automatically takes the fields as a dict and then unpacks it to get the necessary result
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@app.post("/new_status", response_model=schemas.Status)
def add_status(post: schemas.Status, db: Session = Depends(get_db)):
    data = models.Status(**post.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data
