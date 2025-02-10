from manim import *
from manim_slides import Slide
from .constants import *
from .proof_scroll import *


arrow_style = {"stroke_width": 6, "stroke_color": BLUE}


class ProofDiagramBox(Group):
    def __init__(
        self,
        label="",
        width=3.2,
        height=3.4,
        corner_radius=0.25,
        text_scale=1,
        text_buff=0.2,
        **kwargs
    ):

        super().__init__()
        self.rect = RoundedRectangle(
            corner_radius=corner_radius,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=BLACK,
            width=width,
            height=height,
            # stroke_width=6,
            **kwargs
        )
        self.text = (
            Paragraph(label, alignment="center", **TALK_BODY_TEXT)
            .align_to(self.rect, UP)
            .shift(DOWN * text_buff)
            .scale(text_scale)
        )
        self.add(self.rect)
        self.add(self.text)


class Solver(ProofDiagramBox):
    def __init__(self, **kwargs):
        super().__init__("CP Solver", **kwargs)
        self.gears = (
            ImageMobject("img/gears.png")
            .scale(0.58)
            .align_to(self.rect, DOWN)
            .shift(UP * 0.34)
        )
        self.add(self.gears)


class LineGroup(VGroup):
    def __init__(self, left, right, num=3, buff=0.2, **kwargs):
        super().__init__(**kwargs)
        lines = VGroup(
            *[
                Line(left + [buff, 0, 0], right - [buff, 0, 0], stroke_color=BLACK)
                for _ in range(num)
            ]
        )
        self.add(lines.arrange(DOWN))
        self.arrange(DOWN)


class ProblemDescription(ProofDiagramBox):
    def __init__(self, **kwargs):
        super().__init__(
            "Problem\nDescription",
            text_scale=0.6,
            corner_radius=0,
            width=2.1,
            height=2.3,
            **kwargs
        )
        lines = LineGroup(self.rect.get_left(), self.rect.get_right(), num=3)
        self.add(lines.shift(DOWN * 0.5))


class Checker(ProofDiagramBox):
    def __init__(self, **kwargs):
        super().__init__(
            "Independent\nProof\nChecker",
            text_scale=0.6,
            text_buff=0.0,
            width=2.2,
            height=3,
            **kwargs
        )
        gears = (
            ImageMobject("img/checker.png")
            .scale(0.25)
            .align_to(self.rect, DOWN)
            .shift(UP * 0.25)
        )
        self.add(gears)


class ProofScroll(Group):
    def __init__(self, width=1.8, height=2.2, **kwargs):
        super().__init__(**kwargs)
        self.scroll = Scroll(width=width, height=height, tube_height=0.2)

        self.header = (
            Text("Proof", **TALK_BODY_TEXT)
            .scale(0.8)
            .next_to(self.scroll.get_body_top(), DOWN, buff=0.2)
        )

        self.lines = LineGroup(
            self.scroll.get_body_left(), self.scroll.get_body_right(), num=6
        )

        self.add(self.scroll)
        self.add(self.header)
        self.add(self.lines.shift(DOWN * 0.4))


class DiagramArrow(Line):
    def __init__(self, left, right, center_of_first=False, tip=True, **kwargs):
        if isinstance(left, Mobject):
            left = left.get_right()

        if isinstance(right, Mobject):
            right = right.get_left()

        if not center_of_first:
            super().__init__([left[0], right[1], 0], right, **arrow_style, **kwargs)
        else:
            super().__init__(left, [right[0], left[1], 0], **arrow_style, **kwargs)
        if tip:
            self.add_tip()


class Answer(ProofDiagramBox):
    def __init__(self):
        super().__init__(
            "Untrusted\nAnswer",
            corner_radius=0,
            text_scale=0.7,
            width=2.5,
            height=1.2,
            text_buff=0.1,
        )


class ProofDiagram(Group):
    def __init__(self):
        super().__init__()

        self.show_counter = 0

        self.problem = ProblemDescription().shift(LEFT * 5.5)

        self.solver = Solver().shift(LEFT * 1.7)

        self.proof = ProofScroll().shift(RIGHT * 2 + DOWN * 1.2)

        self.answer = (
            Answer()
            .shift(RIGHT * 2 + UP * 1.3)
            .align_to(self.proof.scroll.get_body_left(), LEFT)
        )

        self.checker = Checker().shift(RIGHT * 5.5 + DOWN * 1.8)

        self.arrow1 = DiagramArrow(self.problem, self.solver)

        self.arrow2a = Line(
            self.arrow1.get_center(),
            self.arrow1.get_center() + DOWN * 3 + RIGHT * 0.028,
            **arrow_style
        )

        self.arrow2b = DiagramArrow(
            self.arrow1.get_center() + DOWN * 3, self.checker, center_of_first=True
        )

        self.arrow3 = DiagramArrow(self.solver, self.answer)
        self.arrow4 = DiagramArrow(self.solver, self.proof.scroll.get_body_left())
        self.arrow5 = DiagramArrow(self.proof.scroll.get_body_right(), self.checker)

        self.arrow6a = DiagramArrow(
            self.answer, self.checker.get_center(), center_of_first=True, tip=False
        )
        self.arrow6b = Line(
            self.arrow6a.end + UP * 0.028, self.checker.get_top(), **arrow_style
        ).add_tip()

        self.add(self.arrow1)
        self.add(self.arrow2a)
        self.add(self.arrow2b)
        self.add(self.arrow3)
        self.add(self.arrow4)
        self.add(self.arrow5)
        self.add(self.arrow6a)
        self.add(self.arrow6b)
        self.add(self.problem)
        self.add(self.solver)
        self.add(self.proof)
        self.add(self.answer)
        self.add(self.checker)

        self.show_anims = [
            FadeIn(self.problem),
            AnimationGroup(
                GrowFromPoint(self.arrow1, self.arrow1.start), FadeIn(self.solver)
            ),
            AnimationGroup(
                GrowFromPoint(self.arrow3, self.arrow3.start), FadeIn(self.answer)
            ),
            AnimationGroup(
                GrowFromPoint(self.arrow4, self.arrow4.start),
                GrowFromCenter(self.proof),
            ),
            AnimationGroup(
                LaggedStart(
                    AnimationGroup(
                        GrowFromPoint(
                            self.arrow2a,
                            self.arrow2a.start,
                            rate_func=rate_functions.ease_in_sine,
                        ),
                        GrowFromPoint(
                            self.arrow6a,
                            self.arrow6a.start,
                            rate_func=rate_functions.ease_in_sine,
                        ),
                    ),
                    AnimationGroup(
                        GrowFromPoint(
                            self.arrow2b,
                            self.arrow2b.start,
                            rate_func=rate_functions.ease_out_sine,
                        ),
                        GrowFromPoint(
                            self.arrow6b,
                            self.arrow6b.start,
                            rate_func=rate_functions.ease_out_sine,
                        ),
                        GrowFromPoint(self.arrow5, self.arrow5.start),
                        FadeIn(self.checker),
                    ),
                    lag_ratio=1,
                ),
            ),
        ]

    def next_anim(self):
        self.show_counter += 1
        return self.show_anims[self.show_counter - 1]

    def has_next(self):
        return self.show_counter < len(self.show_anims)
