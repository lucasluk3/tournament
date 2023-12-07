from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from core.database_connection import Base


class Tournament(Base):
    __tablename__ = 'tournaments'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(100))
    total_matches = Column(Integer, default=0)
    total_rounds = Column(Integer, default=0)
    is_started = Column(Boolean, default=False)

    competitors = relationship('Competitor', back_populates='tournament')
    matches = relationship('Match', back_populates='tournament')
    podium = relationship('Podium', back_populates='tournament')
