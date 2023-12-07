from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from core.database_connection import Base


class Competitor(Base):
    __tablename__ = "competitors"
    __table_args__ = (
        UniqueConstraint("name", "tournament_id", name="name_tournament_uc"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String,  nullable=True)

    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=True)
    tournament = relationship("Tournament", back_populates="competitors", lazy="joined")

