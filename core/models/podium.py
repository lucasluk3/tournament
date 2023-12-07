from sqlalchemy.orm import relationship

from core.database_connection import Base

from sqlalchemy import Column, Integer, ForeignKey


class Podium(Base):
    __tablename__ = "podium"

    id = Column(Integer, primary_key=True)

    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    tournament = relationship("Tournament", back_populates="podium")

    first_place_id = Column(Integer, ForeignKey("competitors.id"))
    second_place_id = Column(Integer, ForeignKey("competitors.id"))
    third_place_id = Column(Integer, ForeignKey("competitors.id"))
    fourth_place_id = Column(Integer, ForeignKey("competitors.id"))

    first_place = relationship("Competitor", foreign_keys=first_place_id)
    second_place = relationship("Competitor", foreign_keys=second_place_id)
    third_place = relationship("Competitor",  foreign_keys=third_place_id)
    fourth_place = relationship("Competitor", foreign_keys=fourth_place_id)
