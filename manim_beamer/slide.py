from manim import *
from manim_slides import Slide

from .constants import *


class TalkSlide(Slide):
    def reveal_in_sequence(self, group, **kwargs):
        for g in group:
            if isinstance(g, Mobject):
                self.next_slide()
                self.play(FadeIn(g, **kwargs))
            else:
                self.next_slide()
                self.play(*[FadeIn(m, **kwargs) for m in g])
