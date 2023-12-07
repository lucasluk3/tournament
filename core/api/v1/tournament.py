import math
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import func

from core.database_connection import get_db
from core.models.competitor import Competitor
from core.models.match import Match
from core.models.podium import Podium
from core.models.result import Result
from core.models.tournament import Tournament
from core.schemas.tournament import (
    TournamentBase, CompetitorReadOnly,
    CreateCompetitor, MatchesBase,
    RegisterResult, PodiumSchema
)

router = APIRouter(
    prefix='/tournaments',
    tags=['tournaments'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/', response_model=List[TournamentBase])
async def list_tournaments(db: Session = Depends(get_db)):
    """
    List all tournaments
    """
    query = db.query(Tournament).all()
    return query


@router.post('/', response_model=TournamentBase)
async def create_tournament(tournament: TournamentBase, db: Session = Depends(get_db)):
    """
    Create a new tournament
    """
    tournament_db = Tournament(**tournament.model_dump())
    db.add(tournament_db)
    db.commit()
    db.refresh(tournament_db)
    return tournament_db


@router.post('/{tournament_id}/competitor', response_model=CompetitorReadOnly)
async def create_competitor(
        competitor: CreateCompetitor,
        tournament_id: int,
        db: Session = Depends(get_db)
):
    """
    Create a new competitor in a tournament
    """
    try:
        tournament = db.query(Tournament).filter(Tournament.id == tournament_id).one()
    except NoResultFound:
        return JSONResponse(status_code=404, content='Tournament not found')

    competitor_db = Competitor(
        **competitor.model_dump(), tournament=tournament, tournament_id=tournament_id,
    )
    db.add(competitor_db)
    db.commit()
    db.refresh(competitor_db)
    return competitor


@router.get('/{tournament_id}/generate-matches', response_model=List[MatchesBase])
async def generate_initial_tournament_matches(
        tournament_id: int,
        db: Session = Depends(get_db)
):
    """
    Generate the initial matches of a tournament
    """
    try:
        tournament = db.query(Tournament).filter(Tournament.id == tournament_id).one()
    except NoResultFound:
        return JSONResponse(status_code=404, content='Tournament not found')

    competitors = db.query(Competitor).filter(
        Competitor.tournament_id == tournament_id
    ).order_by(func.random()).all()

    competitors_length = len(competitors)
    if not competitors_length:
        return JSONResponse(status_code=400, content='Is needed register competitors to generate the matches')

    total_rounds = math.frexp(competitors_length)[1]
    tournament.total_matches = competitors_length
    tournament.total_rounds = total_rounds
    db.add(tournament)
    db.commit()
    db.refresh(tournament)

    list_items = []
    for index in range(competitors_length):
        first_competitor_id = competitors[index].id
        second_competitor_id = competitors[competitors_length - index - 1].id

        if first_competitor_id not in list_items and second_competitor_id not in list_items:
            if first_competitor_id == second_competitor_id:
                match = Match(
                    round=total_rounds,
                    match_number=tournament.total_matches,
                    competitor_one_id=first_competitor_id,
                    tournament_id=tournament_id,
                )
            else:
                match = Match(
                    round=total_rounds,
                    match_number=tournament.total_matches,
                    competitor_one_id=first_competitor_id,
                    competitor_two_id=second_competitor_id,
                    tournament_id=tournament_id,
                )
            list_items.append(first_competitor_id)
            list_items.append(second_competitor_id)
            db.add(match)
            db.commit()
            db.refresh(match)

    matches = db.query(Match).filter(Match.tournament_id == tournament_id).all()
    return matches


@router.get('/{tournament_id}/match', response_model=List[MatchesBase])
async def list_matches(
        tournament_id: int,
        db: Session = Depends(get_db)
):
    """
    List all matches of a tournament
    """
    matches = db.query(Match).filter(Match.tournament_id == tournament_id).filter(Match.results.is_(None)).all()
    return matches


@router.post('/{tournament_id}/match/{match_id}/', response_model=MatchesBase)
async def register_match_result(
        tournament_id: int,
        match_id: int,
        result: RegisterResult,
        db: Session = Depends(get_db)
):
    """
    Register the result of a match of a tournament and prepares the next round
    """
    try:
        tournament = db.query(Tournament).filter(Tournament.id == tournament_id).one()
    except NoResultFound:
        return JSONResponse(status_code=404, content='Tournament not found')

    try:
        match = db.query(Match).filter(Match.id == match_id, Match.tournament_id == tournament_id).one()
    except NoResultFound:
        return JSONResponse(status_code=404, content='Match not found')

    if result.winner_id == match.competitor_one_id:
        loser = match.competitor_two
    else:
        loser = match.competitor_one

    result = Result(**result.model_dump(), match=match,  match_id=match_id, loser=loser)
    db.add(result)
    db.commit()
    db.refresh(result)

    if match.status == 'third_place':
        podium = Podium(
            tournament_id=tournament_id,
            third_place_id=result.winner.id,
            fourth_place_id=result.loser.id,
        )
        db.add(podium)
        db.commit()
        db.refresh(podium)
    if match.status == 'final':
        podium = db.query(Podium).filter(Podium.tournament_id == tournament_id).one()
        podium.first_place = result.winner
        podium.second_place = result.loser
        db.add(podium)
        db.commit()
        db.refresh(podium)

    third_place_match = None
    if tournament.total_rounds == 3:
        try:
            third_place_match = db.query(Match).filter(
                Match.round == 2,
                Match.tournament_id == tournament_id,
                Match.status == 'third_place',
                Match.competitor_two.is_(None)
            ).one()
        except NoResultFound:
            third_place_match = Match(
                match_number=tournament.total_matches,
                status='third_place',
                round=2,
                competitor_one_id=None,
                competitor_two_id=None,
                tournament_id=tournament_id,
            )
        if third_place_match.competitor_one is None:
            third_place_match.competitor_one = result.loser
        else:
            third_place_match.competitor_two = result.loser

        db.add(third_place_match)
        db.commit()
        db.refresh(third_place_match)

    if len(tournament.competitors) // tournament.total_matches == tournament.total_matches // 2:
        tournament.total_rounds -= 1
        db.add(tournament)
        db.commit()
        db.refresh(tournament)
    try:
        next_match = db.query(Match).filter(
            Match.tournament_id == tournament_id,
            Match.status != 'third_place',
        ).filter(or_(Match.competitor_one.is_(None), Match.competitor_two.is_(None))).one()
        next_match.match_number = tournament.total_matches
    except NoResultFound:
        next_match = Match(
            round=tournament.total_rounds if not third_place_match else tournament.total_rounds - 2,
            status='final' if third_place_match else '',
            match_number=tournament.total_matches,
            competitor_one_id=None,
            competitor_two_id=None,
            tournament_id=tournament_id,
        )
    if next_match.competitor_one is None:
        next_match.competitor_one = result.winner
    else:
        next_match.competitor_two = result.winner

    tournament.total_matches -= 1
    db.add(tournament)
    db.commit()
    db.refresh(tournament)

    db.add(next_match)
    db.commit()
    db.refresh(next_match)
    return match


@router.get('/{tournament_id}/results/', response_model=PodiumSchema)
def get_tournament_podium(
        tournament_id: int,
        db: Session = Depends(get_db)
):
    """
    Get the podium of a tournament
    """
    try:
        podium = db.query(Podium).filter(Podium.tournament_id == tournament_id).one()
    except NoResultFound:
        return JSONResponse(status_code=404, content='Podium not found')
    return podium
