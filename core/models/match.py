from core.database_connection import Base

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.orm import relationship


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    round = Column(Integer, default=0)
    match_number = Column(Integer, default=0)
    status = Column(String, default='')

    tournament_id = Column(Integer,  ForeignKey("tournaments.id"))
    tournament = relationship("Tournament", back_populates="matches")

    competitor_one_id = Column(Integer, ForeignKey("competitors.id"))
    competitor_two_id = Column(Integer, ForeignKey("competitors.id"))

    competitor_one = relationship("Competitor", foreign_keys=competitor_one_id)
    competitor_two = relationship("Competitor", foreign_keys=competitor_two_id)

    results = relationship("Result", back_populates="match")

