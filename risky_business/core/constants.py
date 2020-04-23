from enum import Enum


class AUPDecisionChoices(Enum):
    ALLOW = 'Allow'
    REJECT = 'Reject'
    ALERT = 'Alert'


class LanguageChoices(Enum):
    ENGLISH = 'EN'
    FINNISH = 'FI'
    GERMAN = 'DE'


class SpacyPatternKeys(Enum):
    LOWER = 'LOWER'
    LENGTH = 'LENGTH'
    IS_ALPHA = 'IS_ALPHA'
    IS_ASCII = 'IS_ASCII'
    IS_DIGIT = 'IS_DIGIT'
    IS_PUNCT = 'IS_PUNCT'
    IS_SPACE = 'IS_SPACE'
    IS_LOWER = 'IS_LOWER'
    IS_UPPER = 'IS_UPPER'
    IS_TITLE = 'IS_TITLE'
    IS_STOP = 'IS_STOP'
    LIKE_NUM = 'LIKE_NUM'
    LIKE_URL = 'LIKE_URL'
    LIKE_EMAIL = 'LIKE_EMAIL'
    POS = 'POS'
    TAG = 'TAG'
    DEP = 'DEP'
    LEMMA = 'LEMMA'
    SHAPE = 'SHAPE'
    ENT_TYPE = 'ENT_TYPE'