from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from . import models, schemas


def get_resource(db: Session, resource_uuid: str):
    return db.query(models.Resource).filter(models.Resource.uuid == resource_uuid).first()


def get_resources(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resource).filter(models.Resource.active == True).offset(skip).limit(limit).all()


def create_resource(db: Session, resource: schemas.ResourceCreate):
    resource_uuid = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    active = True
    db_resource = models.Resource(
        uuid=resource_uuid,
        timestamp=timestamp,
        active=active,
        **resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


def remove_resource(db: Session, resource_uuid: str):
    db_resource = db.query(models.Resource).filter(
        models.Resource.uuid == resource_uuid)
    db_resource.update({"active": False})
    db.commit()
    db.refresh(db_resource.first())
    return db_resource.first()
