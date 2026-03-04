from datetime import date
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, computed_field, Field


class BasePlayer(BaseModel):
    first_name: str
    last_name: str


class ResponsePlayer(BasePlayer):
    id: int


class CreatePlayer(BasePlayer):
    ...


class UpdatePlayer(BasePlayer):
    ...


class PartialPlayer(BasePlayer):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ResponsePlayerCompetition(BaseModel):
    id: int
    name: str
    date: date
    rating: Optional[int]
    diff: Optional[int]
    matches_diff: Optional[int]
    wins_diff: Optional[int]
    losses_diff: Optional[int]
    description: Optional[str] = None
    goals_diff: Optional[int] = 0
    place: Optional[int] = 0
    cumulative: Optional[int] = 0
    cumulative_diff: Optional[int] = 0

    @computed_field
    def date_str(self) -> str:

        return self.date.strftime('%d.%m.%Y')


class ResponsePlayerCompetitionList(BaseModel):
    """Список игроков с рейтингом"""
    count: int
    competitions: List[ResponsePlayerCompetition]


class ResponcePlayerInfo(BaseModel):
    rating: int
    matches: int
    wins: int
    losses: int
    first_name: str
    last_name: str


class ResponceMatchRow(BaseModel):
    id: int
    is_qualification: bool
    rating: int
    diff: Optional[int]
    wins_diff: Optional[int]
    losses_diff: Optional[int]
    score: Optional[str]
    color: Optional[str]
    left_team_first_id: Optional[int]
    left_team_first: Optional[str]
    left_team_second_id: Optional[int]
    left_team_second: Optional[str]
    right_team_first_id: Optional[int]
    right_team_first: Optional[str]
    right_second_id: Optional[int]
    right_second: Optional[str]


class PartnerResponce(BaseModel):
    id: int
    is_win: bool
    is_losse: bool
    count: int
    name: str


class PlayerStatisticResponce(BaseModel):
    id: int
    name: str
    rating: int
    matches: Optional[int] = 0
    wins: Optional[int] = 0
    losses: Optional[int] = 0
    draws: Optional[int] = 0
    percent_wins: Optional[int] = 0
    competitions_count: Optional[int] = 0
    gold: Optional[int] = 0
    silver: Optional[int] = 0
    bronze: Optional[int] = 0
    rank: Optional[str] = ''
    color: Optional[str] = ''


class SeriesResponce(BaseModel):
    s_wins: int
    s_loss: int
    s_draws: int


class DTFBLicence(Enum):
    A = 'A'
    B = 'B'
    C = 'C'


class SportCategory(Enum):
    JUNIOR = 'junior'
    SENIOR = 'senior'
    MAN = 'men'
    WOMEN = 'women'
    DIVERS = 'non-binary'


class MembershipState(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'


class ClubMembership(BaseModel):
    club: str
    clubCity: str
    membershipState: MembershipState
    association: str


class KTPlayer(BaseModel):
    id: str = Field(..., alias='_id')
    first_name: str = Field(..., alias='firstName')
    last_name: str = Field(..., alias='lastName')
    categories: list[SportCategory]
    club_memberships: list[ClubMembership] = Field(..., alias='clubMemberships')

    birth_year: Optional[int] = Field(None, alias='birthYear')
    country: Optional[str] = 'RF'
    national_id: Optional[str] = Field(None, alias='nationalId')
    international_id: Optional[str] = Field(None, alias='internationalId')
    national_licence: Optional[DTFBLicence] = Field(None, alias='nationalLicence')
