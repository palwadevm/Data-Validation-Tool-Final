from enum import Enum


class Match_Status(Enum):
    FIELDS_MISMATCH = 1
    MISSING_DATA = 2
    MATCHED = 3
