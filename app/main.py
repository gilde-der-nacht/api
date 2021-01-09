from typing import List
from fastapi import FastAPI, Depends, HTTPException
from storage import crud, models, schemas
from sqlalchemy.orm import Session

from storage.storage import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def status():
    return "Olymp is up and running!"


@app.get("/version")
def version():
    return "1.1.0"


@app.get("/resources/", response_model=List[schemas.Resource])
def read_resources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    resources = crud.get_resources(db=db, skip=skip, limit=limit)
    return resources


@app.post("/resources/", response_model=schemas.Resource)
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    return crud.create_resource(db=db, resource=resource)


@app.get("/resources/{resource_uuid}", response_model=schemas.Resource)
def read_resource(resource_uuid: str, db: Session = Depends(get_db)):
    db_resource = crud.get_resource(db=db, resource_uuid=resource_uuid)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource


@app.delete("/resources/{resource_uuid}", response_model=schemas.Resource)
def remove_resource(resource_uuid: str, db: Session = Depends(get_db)):
    return crud.remove_resource(db=db, resource_uuid=resource_uuid)
