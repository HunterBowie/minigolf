from dataclasses import dataclass, field

import pygame

from _windowgui.constants import RelativePosition
from _windowgui.gui.elements.gui_element import GUIElement
from _windowgui.util import Text, TextStyle, root


@dataclass
class TextElement(GUIElement):
    """A GUI element for displaying text."""

    x: int = 0
    y: int = 0
    tag: str = ""
    root_pos: RelativePosition = RelativePosition.TOP_LEFT
    string: str = ""
    style: TextStyle = field(default_factory=TextStyle)
    newline_width: int = None

    def __post_init__(self):
        self.text = Text(
            string=self.string,
            x=self.x,
            y=self.y,
            style=self.style,
            newline_width=self.newline_width,
        )
        self.text.x, self.text.y = root(
            self.text.get_rect(), self.root_pos).topleft
        self.x = self.text.x
        self.y = self.text.y
        self.width = self.text.get_width()
        self.height = self.text.get_height()
        super().__post_init__()

    def update(self):
        pass

    def eventloop(self, event: pygame.event.Event):
        pass

    def render(self, surface: pygame.Surface):
        self.text.render(surface)
