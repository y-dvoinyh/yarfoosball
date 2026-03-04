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

    low_minus = 'Low-'      # -500
    low = 'Low'             # 500-700
    low_plus = 'Low+'       # 700-1000
    mid_minus = 'Mid-'      # 1000-1100
    mid = 'Mid'             # 1100-1200
    mid_plus = 'Mid+'       # 1200-1300
    high_minus = 'High-'    # 1300-1400
    high = 'High'           # 1400-1500
    high_plus = 'High+'     # 1500-1600
    new_pro = 'Pro'         # 1600-1700
    pro_plus = 'Pro+'       # 1700+
