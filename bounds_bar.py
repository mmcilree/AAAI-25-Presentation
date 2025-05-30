from manim import *
from manim_beamer.constants import *

FRAME_WIDTH = config["frame_width"]
FRAME_HEIGHT = config["frame_height"]


class BoundsBar(VGroup):

    def __init__(
        self,
        var_name="X",
        max_bounds=(-5, 4),
        bounds=[(-4, 4), (-3, 2), (-2, 1)],
        **kwargs
    ):
        width = FRAME_WIDTH / 5 * 4
        height = width / 16
        super().__init__()

        self.outer_rect = Rectangle(width=width, height=height, stroke_color=BLACK)

        self.colors = [GRAY, RED, UG_COBALT]
        self.max_bounds = max_bounds
        self.max_range = max_bounds[1] - max_bounds[0]
        self.unit = width / self.max_range
        self.bounds = bounds

        self.fill_rect = {}
        self.labels = {}

        for i, color in enumerate(self.colors):
            self.fill_rect[color] = (
                Rectangle(
                    width=(bounds[i][1] - bounds[i][0]) * self.unit,
                    height=height,
                    fill_color=color,
                    fill_opacity=1,
                    stroke_width=0,
                )
                .align_to(self.outer_rect, LEFT)
                .shift(RIGHT * (bounds[i][0] - max_bounds[0]) * self.unit)
            )
            self.labels[color] = [
                MathTex(str(bounds[i][0]) + r" \leq ", color=BLACK if i == 2 else GRAY)
                .scale(0.9)
                .move_to(self.fill_rect[color].get_corner(UP + LEFT) + UP * 0.3)
                .set_opacity(
                    i == (len(self.colors)) - 1 or bounds[i][0] != bounds[i - 1][0]
                ),
                MathTex(r" \leq " + str(bounds[i][1]), color=BLACK if i == 2 else GRAY)
                .scale(0.9)
                .move_to(self.fill_rect[color].get_corner(UP + RIGHT) + UP * 0.3)
                .set_opacity(
                    i == (len(self.colors) - 1) or bounds[i][1] != bounds[i + 1][1]
                ),
            ]

            self.add(
                self.fill_rect[color],
                self.labels[color][0],
                self.labels[color][1],
            )

        mid = (
            self.labels[UG_COBALT][0].get_center()
            + (
                self.labels[UG_COBALT][1].get_center()
                - self.labels[UG_COBALT][0].get_center()
            )
            / 2
        )
        self.var_label = MathTex(var_name, color=BLACK).move_to(mid)

        self.add(self.outer_rect, self.var_label)

    def update_bounds(self, bounds):
        for i, color in enumerate(self.colors):
            self.fill_rect[color].stretch_to_fit_width(
                (bounds[i][1] - bounds[i][0]) * self.unit
            ).align_to(self.outer_rect, LEFT).shift(
                RIGHT * (bounds[i][0] - self.max_bounds[0]) * self.unit
            )

            self.labels[color][0].become(
                MathTex(
                    str(bounds[i][0]) + r" \leq ",
                    color=BLACK if i == len(self.colors) - 1 else GRAY,
                )
                .scale(0.9)
                .move_to(self.fill_rect[color].get_corner(UP + LEFT) + UP * 0.3)
                .set_opacity(
                    i == len(self.colors) - 1 or bounds[i][0] != bounds[i - 1][0]
                )
            )

            self.labels[color][1].become(
                MathTex(r" \leq " + str(bounds[i][1]), color=BLACK if i == 2 else GRAY)
                .scale(0.9)
                .move_to(self.fill_rect[color].get_corner(UP + RIGHT) + UP * 0.3)
                .set_opacity(
                    i == len(self.colors) - 1 or bounds[i][1] != bounds[i + 1][1]
                )
            )

            mid = (
                self.labels[UG_COBALT][0].get_center()
                + (
                    self.labels[UG_COBALT][1].get_center()
                    - self.labels[UG_COBALT][0].get_center()
                )
                / 2
            )

            self.var_label.move_to(mid)
