from sqlalchemy import Boolean, Column, String

from .storage import Base


class Resource(Base):
    __tablename__ = "resource"

    uuid = Column(String, primary_key=True, index=True)
    timestamp = Column(String, nullable=False)
    description = Column(String, nullable=False)
    url = Column(String, nullable=False)
    active = Column(Boolean, nullable=False)
