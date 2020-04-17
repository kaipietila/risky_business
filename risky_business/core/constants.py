from enum import Enum


class AUPDecisionChoices(Enum):
    ALLOW = 'Allow'
    REJECT = 'Reject'
    ALERT = 'Alert'
