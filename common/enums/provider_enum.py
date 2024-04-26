from enum import auto

from common.enums import StrEnum


class ProviderType(StrEnum):
    SECTION = auto()
    LOCAL = auto()
    ABC = auto()

