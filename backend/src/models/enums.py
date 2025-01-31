from enum import Enum


class RatingType(Enum):
    """Тип записи рейтинга"""
    PLAYER = 'PLAYER'
    LEAGUE = 'LEAGUE'
    TOURNAMENT = 'TOURNAMENT'


class TournamentType(Enum):
    """Типы турниров"""
    DYP = 'DYP'
    TEAM = 'TEAM'
    FAST = 'FAST'


class CompetitionType(Enum):
    """Типы соревнований"""
    TEAM = 'Team-League'
    DYP = 'DYP'
    OS = "Open Singles"
    OD = "Open Dobules"
    WS = "Women Singles"
    WD = "Women Doubles"
    MS = "Men Singles"
    MD = "Men Doubles"
    AS = "Amateur Singles"
    AD = "Amateur Doubles"
    NS = "Novice Singles"
    ND = "Novice Doubles"
    SPS = "Semi-pro Singles"
    SPD = "Semi-pro Doubles"
    BS = "Beginner Singles"
    BD = "Beginner Doubles"
    JS = "Junior Singles"
    JD = "Junior Doubles"
    COD = "Classic Open Doubles"
    MIXED = "Mixed Doubles"
    PROAM = "Pro-Am"


class HistoryRatingLevel(Enum):
    START = 'START'
    MATCH = 'MATCH'
    COMPETITION = 'COMPETITION'


class Rank(Enum):
    beginner = 'beginner'
    novice = 'novice'   # 1000
    amateur = 'amateur' # 1250
    semipro = 'semi-pro'    # 1500
    pro = 'pro'     # 1750
    master = 'master' # 2000
