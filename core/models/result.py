from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from core.database_connection import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)

    match_id = Column(Integer, ForeignKey("matches.id"))
    match = relationship("Match", foreign_keys=match_id, uselist=False, back_populates="results")

    winner_id = Column(Integer, ForeignKey("competitors.id"))
    winner = relationship("Competitor", foreign_keys=winner_id, uselist=False)

    loser_id = Column(Integer, ForeignKey("competitors.id"))
    loser = relationship("Competitor", foreign_keys=loser_id, uselist=False)
