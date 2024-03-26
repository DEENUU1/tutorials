import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"))
    region = relationship("Region", back_populates="cities")
