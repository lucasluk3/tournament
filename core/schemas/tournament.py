from typing import List, Optional

from pydantic import BaseModel, field_validator


class TournamentBase(BaseModel):
    id:  int
    name: str


class TournamentRegistration(BaseModel):
    name: str


class CreateCompetitor(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True


class CompetitorReadOnly(BaseModel):
    id: int
    name: str


class RegisterResult(BaseModel):
    winner_id: int


class ResultBase(BaseModel):
    winner: Optional[CompetitorReadOnly] = None
    loser: Optional[CompetitorReadOnly] = None

    class Config:
        from_attributes = True


class MatchesBase(BaseModel):
    id: int
    competitor_one: CompetitorReadOnly
    competitor_two: Optional[CompetitorReadOnly] = None

    class Config:
        from_attributes = True


class PodiumSchema(BaseModel):
    first_place: Optional[CompetitorReadOnly] = None
    second_place: Optional[CompetitorReadOnly] = None
    third_place: Optional[CompetitorReadOnly] = None
    fourth_place: Optional[CompetitorReadOnly] = None

    class Config:
        from_attributes = True
