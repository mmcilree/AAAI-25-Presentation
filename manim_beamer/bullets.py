from manim import * 
from manim_slides import Slide

from .constants import *

class BulletPoints(VGroup):
    def __init__(self, *text, bullet_style="SQUARE", bullet_color=UG_BLUE, bullet_space=1, line_space=0.5, **kwargs):
        super().__init__()
        bullet_unicode = {
            "SQUARE": "▪",
            "DOT": "•",
            "CIRCLE": "○"
        }
        bulleted_text = ["".join([bullet_unicode[bullet_style], " " + " "*bullet_space, t]).replace("\n", "\n   " + " "*bullet_space) for t in text]

        self.bullet_texts = VGroup(*[MarkupText(b, **kwargs) for b in bulleted_text]).arrange(DOWN, buff=line_space, center=False, aligned_edge=LEFT)

        [b[0].set_color(UG_BLUE) for b in self.bullet_texts]
        self.add(self.bullet_texts)

        self.center()

