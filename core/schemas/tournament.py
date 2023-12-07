from typing import List, Optional

from pydantic import BaseModel


class TournamentBase(BaseModel):
    name: str
    total_matches: int
    total_rounds: int


class CreateCompetitor(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True


class CompetitorReadOnly(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RegisterResult(BaseModel):
    winner_id: int


class ResultBase(BaseModel):
    winner: Optional[CompetitorReadOnly] = None
    loser: Optional[CompetitorReadOnly] = None

    class Config:
        from_attributes = True


class MatchesBase(BaseModel):
    id: int
    match_number: Optional[int] = None
    tournament: TournamentBase
    competitor_one: CompetitorReadOnly
    competitor_two: Optional[CompetitorReadOnly] = None
    # result: ResultBase

    class Config:
        from_attributes = True


class PodiumSchema(BaseModel):
    id:  int
    first_place: Optional[CompetitorReadOnly] = None
    second_place: Optional[CompetitorReadOnly] = None
    third_place: Optional[CompetitorReadOnly] = None
    fourth_place: Optional[CompetitorReadOnly] = None

    class Config:
        from_attributes = True
