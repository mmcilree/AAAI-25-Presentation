from manim import *
from manim_slides import Slide
from manim_beamer import *
from .constants import *


class SmartTable(Table):
    def __init__(self, entries, col_labels=None):
        self.num_rows = len(entries) + (1 if col_labels else 0)
        self.num_cols = len(entries[0])
        self.col_labels = (
            None
            if col_labels is None
            else [MathTex(c, color=WHITE) for c in col_labels]
        )
        super().__init__(
            entries,
            col_labels=self.col_labels,
            element_to_mobject=MathTex,
            element_to_mobject_config={"color": BLACK},
            line_config={"stroke_color": BLACK},
            include_outer_lines=True,
        )

        for i in range(1, len(col_labels) + 1):
            self.add_highlighted_cell((1, i), color=UG_BLUE, fill_opacity=1)

        for i in range(2, len(entries) + 2):
            for j in range(1, len(entries[0]) + 1):
                self.add_highlighted_cell((i, j), color=WHITE, fill_opacity=1)

    def get_cell_background(self, i, j):
        total_cells = self.num_rows * self.num_cols
        pos = i * self.num_cols + j
        return self[total_cells - pos - 1]
