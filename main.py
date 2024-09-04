import time
import psycopg2
from fastapi import FastAPI, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor

import models, schemas
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


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    data = db.query(models.Devices).all()
    return data


@app.get("/get/{Id}")
def device_selected(Id: int, db: Session = Depends(get_db)):
    device = db.query(models.Devices).filter(models.Devices.id == Id).first()

    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {Id} not found")


@app.post("/device", response_model=schemas.Devices)
def add_device(post: schemas.Devices, db: Session = Depends(get_db)):
    # new_post = models.Posts(title=post.title, content=post.content, published=post.published) is same as below
    new_post = models.Devices(**post.dict())  # ** unpacks the dict
    # It automatically takes the fields as a dict and then unpacks it to get the necessary result
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
