from enum import Enum

class Choices(Enum):
    @classmethod
    def choices(cls):
        return tuple((choice.name, choice.value) for choice in cls)