from __future__ import annotations

from enum import Enum, auto

import pygame

HELD_DIST_Y = 20
HELD_DIST_X = 100

FADE_TIME = 0.5
FADE_SPEED = 10


class ButtonStatus(Enum):
    DOWN = "down"
    UP = "up"


class ButtonImageShape(Enum):
    SQUARE = "square"
    LONG = "long"


class AssetType(Enum):
    IMAGES = auto()
    SOUND = auto()
    FONT = auto()


class ColorStyle(Enum):
    WHITE = "white"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"


class CheckBoxType(Enum):
    TICK_SYMBOL = "tick"
    CROSS_SYMBOL = "cross"
    CHECK_SYMBOL = "checkmark"


class EventType:
    """Pygame events used with the GUI."""

    _NAMES = [
        "BUTTON_CLICKED",
        "BUTTON_RELEASED",
        "CHECKBOX_CLICKED",
        "TEXTBOX_POSTED",
        "TEXTBOX_SELECTED",
    ]

    BUTTON_CLICKED = pygame.USEREVENT + _NAMES.index("BUTTON_CLICKED")
    BUTTON_RELEASED = pygame.USEREVENT + _NAMES.index("BUTTON_RELEASED")
    CHECKBOX_CLICKED = pygame.USEREVENT + _NAMES.index("CHECKBOX_CLICKED")
    TEXTBOX_POSTED = pygame.USEREVENT + _NAMES.index("TEXTBOX_POSTED")
    TEXTBOX_SELECTED = pygame.USEREVENT + _NAMES.index("TEXTBOX_SELECTED")
    # TEXTBOX_MOVED = pygame.USEREVENT + _NAMES.index("MOVED")

    ALL = [
        BUTTON_CLICKED,
        BUTTON_RELEASED,
        CHECKBOX_CLICKED,
        TEXTBOX_POSTED,
        TEXTBOX_SELECTED,
    ]

    @classmethod
    def get_name(cls, event_type):
        return cls.NAMES[cls.ALL.index(event_type)]
