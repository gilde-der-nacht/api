from pydantic import BaseModel


class ResourceBase(BaseModel):
    description: str
    url: str


class Resource(ResourceBase):
    uuid: str
    timestamp: str
    active: bool

    class Config:
        orm_mode = True


class ResourceCreate(ResourceBase):
    pass
