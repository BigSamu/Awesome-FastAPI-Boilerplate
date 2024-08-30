from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class Survey(Base):
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    image_url = Column(String(255), nullable=False)
    provider = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    reference_number = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    def __repr__(self):
        return ("<Survey {self.id}, reference number: {self.reference_number}, location: {self.location}, provider: {self.provider}>").format(self=self)
