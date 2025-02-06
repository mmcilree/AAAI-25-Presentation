from manim import *
from manim_slides import Slide

from .constants import *


class Tube(VGroup):
    def __init__(
        self,
        width=4,
        height=0.8,
        stroke_color=WHITE,
        fill_color=BLACK,
        fill_opacity=1,
        **kwargs
    ):
        super().__init__()
        self.bar = Rectangle(width=width, height=height)

        self.right_cut = ArcBetweenPoints(
            self.bar.get_corner(UP + RIGHT), self.bar.get_corner(DOWN + RIGHT), angle=PI
        )
        self.left_circle = Circle(
            radius=height * 0.5, fill_color=fill_color, fill_opacity=1, stroke_width=0
        ).move_to(self.bar.get_left())

        self.bar_cut = Cutout(
            self.bar,
            self.right_cut,
            fill_color=fill_color,
            fill_opacity=1,
            stroke_width=0,
        )

        self.left_curve = ArcBetweenPoints(
            self.bar.get_corner(UP + LEFT),
            self.bar.get_corner(DOWN + LEFT),
            angle=PI,
            stroke_color=stroke_color,
            fill_opacity=0,
        )

        self.right_curve = ArcBetweenPoints(
            self.bar.get_corner(UP + RIGHT),
            self.bar.get_corner(DOWN + RIGHT),
            angle=PI,
            stroke_color=stroke_color,
        )

        self.top_line = Line(
            self.bar.get_corner(UP + LEFT),
            self.bar.get_corner(UP + RIGHT),
            stroke_color=stroke_color,
        )

        self.bottom_line = Line(
            self.bar.get_corner(DOWN + LEFT),
            self.bar.get_corner(DOWN + RIGHT),
            stroke_color=stroke_color,
        )

        self.add(
            self.bar_cut,
            self.left_circle,
            self.left_curve,
            self.top_line,
            self.right_curve,
            self.bottom_line,
        )


class Scroll(VGroup):
    def __init__(
        self,
        width=4,
        height=5.5,
        tube_height=0.6,
        stroke_color=WHITE,
        fill_color=BLACK,
        fill_opacity=1,
        **kwargs
    ):
        super().__init__()

        fill_hsv = list(fill_color.to_hsv())
        fill_hsv[2] -= 0.15

        darker_color = ManimColor.from_hsv(fill_hsv)
        self.body_fill = Rectangle(
            width=width,
            height=height,
            stroke_width=0,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            **kwargs
        )

        self.right_line = Line(
            [width * 0.5, height * 0.5, 0],
            [width * 0.5, height * -0.5, 0],
            stroke_color=stroke_color,
        )

        self.left_line = Line(
            [-width * 0.5, height * 0.5, 0],
            [-width * 0.5, height * -0.5, 0],
            stroke_color=stroke_color,
        )

        self.top_backing_tube = (
            Tube(
                width=width,
                height=tube_height,
                stroke_color=stroke_color,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                **kwargs
            )
            .shift(UP * height * 0.5)
            .flip(UP)
        )

        self.top_tube = (
            Tube(
                width=width,
                height=tube_height,
                stroke_color=stroke_color,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                **kwargs
            )
            .shift(UP * height * 0.5)
            .shift(LEFT * tube_height * 0.5)
        )

        self.inner_top_tube = (
            Tube(
                width=width,
                height=tube_height * 0.5,
                stroke_color=stroke_color,
                fill_color=darker_color,
                fill_opacity=fill_opacity,
                **kwargs
            )
            .shift(UP * (height * 0.5 - tube_height * 0.25))
            .flip(axis=UP)
            .shift(LEFT * tube_height * 0.25)
        )

        self.bottom_backing_tube = (
            Tube(
                width=width,
                height=tube_height,
                stroke_color=stroke_color,
                fill_color=darker_color,
                fill_opacity=fill_opacity,
                **kwargs
            )
            .shift(DOWN * height * 0.5)
            .shift(RIGHT * tube_height)
            .flip(UP)
        )

        self.bottom_tube = (
            Tube(
                width=width,
                height=tube_height,
                stroke_color=stroke_color,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                **kwargs
            )
            .shift(DOWN * height * 0.5)
            .shift(RIGHT * tube_height * 0.5)
        )

        sq = Square(tube_height * 0.5)
        line_d = {"angle": 0, "color": stroke_color}
        self.inner_bottom_tube = ArcPolygon(
            sq.get_corner(UP + LEFT),
            sq.get_corner(DOWN + LEFT),
            sq.get_corner(DOWN + RIGHT),
            sq.get_corner(UP + RIGHT),
            arc_config=[line_d, line_d, {"angle": -PI, "color": stroke_color}, line_d],
            stroke_color=stroke_color,
            color=fill_color,
            fill_opacity=1,
        )

        self.inner_bottom_tube.move_to(
            self.body_fill.get_corner(DOWN + RIGHT)
            - self.inner_bottom_tube.get_corner(DOWN + LEFT)
        )

        self.add(
            self.bottom_backing_tube,
            self.bottom_tube,
            self.top_backing_tube,
            self.body_fill,
            self.inner_bottom_tube,
            self.left_line,
            self.right_line,
            self.inner_top_tube,
            self.top_tube,
        )

    def get_body_top(self):
        return [self.body_fill.get_center()[0], self.top_tube.get_bottom()[1], 0]

    def get_body_bottom(self):
        return [self.body_fill.get_center()[0], self.bottom_tube.get_bottom()[1], 0]

    def get_body_left(self):
        return self.body_fill.get_left()

    def get_body_right(self):
        return self.body_fill.get_right()

    def get_body_top_left(self):
        return self.body_fill.get_corner(UP + LEFT)

    def get_body_height(self):
        return self.get_body_top()[1] - self.get_body_bottom()[1]

    def get_body_width(self):
        return self.get_body_right()[0] - self.get_body_left()[0]


class ScrollWithTex(Group):
    def __init__(self, tex_strings, vbuff=0.4, buff=0.3, **kwargs):
        super().__init__()
        self.scroll = Scroll(**kwargs)
        self.content = Group(*[MathTex(s, color=WHITE) for s in tex_strings]).arrange(
            DOWN, buff=vbuff
        )

        if self.content.width > self.scroll.get_body_width() - 2 * buff:
            self.content.scale_to_fit_width((self.scroll.get_body_width() - 2 * buff))

        if self.content.height > self.scroll.get_body_height() - 2 * buff:

            self.content.scale(
                (self.scroll.get_body_height() - 2 * buff) / self.content.height
            )

        self.content.next_to(self.scroll.get_body_top(), DOWN, buff=buff)

        [
            g.align_to(self.scroll.get_body_left() + RIGHT * buff, LEFT)
            for g in self.content
        ]
        self.add(self.scroll, self.content)

    def add_content(self, tex_strings, buff=0.25):
        for t in tex_strings:
            self.content.add(
                MathTex(t, color=WHITE)
                .scale_to_fit_height(self.content[0].height)
                .next_to(self.content[-1], DOWN, buff=buff)
                .align_to(self.content[0], LEFT)
            )
