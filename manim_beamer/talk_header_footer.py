from manim import *
from manim_slides import Slide

from .constants import *


FRAME_WIDTH = config["frame_width"]
FRAME_HEIGHT = config["frame_height"]


class HeaderFooter(Group):
    def _get_slide_count(self):
        return sum([self.dots_per_sec[s] for s in self.dots_per_sec])

    def _create_header(self, dots_per_sec):
        self.h_background = Rectangle(
            width=config["frame_width"],
            height=config["frame_height"] / 17,
            fill_color=UG_BLUE,
            color=UG_BLUE,
            fill_opacity=1,
        ).to_edge(UP, 0)

        self.h_background2 = Rectangle(
            width=config["frame_width"],
            height=config["frame_height"] / 10,
            fill_color=UG_COBALT,
            color=UG_COBALT,
            fill_opacity=1,
        ).to_edge(UP, 0)

        self.sections = list(dots_per_sec)
        self.dots_per_sec = dots_per_sec
        self.current_section = self.sections[0]
        self.current_dot = 0
        self.current_section_number = 0

        self.title_texts = dict(
            zip(
                self.sections,
                [
                    Text(sec, color=WHITE, font_size=36, font=CMU_SANS, weight="BOLD")
                    .scale(0.35)
                    .set_opacity(0.5)
                    for sec in self.sections
                ],
            )
        )

        # Even spacing between section titles
        total_title_width = sum([t.width for t in self.title_texts.values()])
        buff = (
            config["frame_width"]
            - total_title_width
            - DEFAULT_MOBJECT_TO_EDGE_BUFFER * 2
        ) / (len(self.sections) - 1)

        self.title_texts[self.current_section].set_opacity(1)

        self.title_group = (
            Group(*self.title_texts.values())
            .arrange(aligned_edge=UP, buff=buff)
            .to_edge(UP, buff=0.08)
            .to_edge(LEFT)
        )

        self.dots = dict(
            zip(
                list(self.sections),
                [
                    VGroup(
                        *[
                            Circle(
                                color=WHITE,
                                radius=0.05,
                                stroke_width=1.5,
                                stroke_opacity=0.5,
                            )
                            for i in range(self.dots_per_sec[sec])
                        ]
                    ).arrange(buff=0.03)
                    for sec in self.sections
                ],
            )
        )

        for sec in self.sections:
            self.dots[sec].move_to(
                self.title_texts[sec].get_left() - self.dots[sec].get_left()
            ).shift(DOWN * 0.2 + RIGHT * 0.01)

        [d.set_stroke(opacity=1) for d in self.dots[self.current_section]]
        self.dots[self.current_section][self.current_dot].set_fill(WHITE, opacity=1)

        self.add(
            self.h_background2, self.h_background, self.title_group, *self.dots.values()
        )

    def _create_footer(self, dots_per_sec, title, name):
        self.f_background = Rectangle(
            width=config["frame_width"],
            height=config["frame_height"] / 26,
            fill_color=UG_BLUE,
            color=UG_BLUE,
            fill_opacity=1,
        ).to_edge(DOWN, 0)

        self.f_background2 = Rectangle(
            width=config["frame_width"],
            height=config["frame_height"] / 13,
            fill_color=UG_COBALT,
            color=UG_COBALT,
            fill_opacity=1,
        ).to_edge(DOWN, 0)

        self.title_text = (
            Text(title, color=WHITE, font=CMU_SANS, font_size=38, weight=BOLD)
            .scale(0.4)
            .move_to(self.f_background)
            .to_edge(LEFT)
        )

        to_midpoint = (
            self.f_background2.get_top()
            - (self.f_background2.height - self.f_background.height) / 2
        )

        self.name_text = (
            Text(name, color=WHITE, font=CMU_SANS, font_size=38, weight=BOLD)
            .scale(0.4)
            .move_to(to_midpoint)
            .to_edge(LEFT)
        )
        total_frames = self._get_slide_count()

        self.count_text = (
            Text(
                "1/" + str(total_frames),
                color=WHITE,
                font=CMU_SANS,
                font_size=38,
                weight=BOLD,
            )
            .scale(0.4)
            .move_to(self.f_background)
            .to_edge(RIGHT)
        )

        self.add(
            self.f_background2,
            self.f_background,
            self.title_text,
            self.name_text,
            self.count_text,
        )

    def __init__(self, dots_per_sec, title="Your Title", name="Your Name", **kwargs):
        super().__init__(**kwargs)

        self._create_header(dots_per_sec)
        self._create_footer(dots_per_sec, title, name)

    def set_current(self, section, dot_number):
        animations = []
        if isinstance(section, int):
            section = self.sections[section]

        self.title_texts[self.current_section].set_opacity(0.5)
        [d.set_stroke(opacity=0.5) for d in self.dots[self.current_section]]
        self.dots[self.current_section][self.current_dot].set_fill(opacity=0.01)

        self.current_section = section
        self.current_section_number = self.sections.index(section)
        self.current_dot = dot_number
        self.title_texts[self.current_section].set_opacity(1)

        current_frame = (
            sum(
                [
                    self.dots_per_sec[self.sections[i]]
                    for i in range(len(self.sections))
                    if i < self.current_section_number
                ]
            )
            + self.current_dot
            + 1
        )
        total_frames = self._get_slide_count()

        self.count_text.become(
            Text(
                str(current_frame) + "/" + str(total_frames),
                color=WHITE,
                font=CMU_SANS,
                font_size=38,
            )
            .scale(0.4)
            .move_to(self.count_text)
        )
        [d.animate.set_stroke(opacity=1) for d in self.dots[self.current_section]]
        self.dots[self.current_section][self.current_dot].set_fill(WHITE, opacity=1)

    def next(self):
        if self.current_dot == self.dots_per_sec[self.current_section] - 1:
            return self.set_current(self.current_section_number + 1, 0)
        else:
            return self.set_current(self.current_section_number, self.current_dot + 1)


class SlideTitle(Text):
    def __init__(self, text, **kwargs):
        super().__init__(
            text, color=BLACK, font=CMU_SANS, font_size=40, weight=BOLD, **kwargs
        )
        self.scale(0.8)
        self.to_edge(LEFT)
        self.align_to([0, 2.9, 0], direction=UP)


class TitleSlide(Group):
    def __init__(self, title, venue="", author="Matthew McIlree", **kwargs):
        super().__init__(**kwargs)
        background = ImageMobject("./img/university.jpg")
        background.width = FRAME_WIDTH
        title_bar = Rectangle(
            width=FRAME_WIDTH, height=FRAME_HEIGHT * 0.4, color=UG_BLUE, fill_opacity=1
        ).to_edge(UP, buff=0)

        white_text_style = {"color": WHITE, "font": CMU_SANS}

        keyline = ImageMobject("./img/UoG_keyline.png")
        keyline.width = FRAME_WIDTH / 3.8
        keyline.to_corner(UP + RIGHT)

        ra_logo = ImageMobject("./img/ra_logo.png")
        ra_logo.width = FRAME_WIDTH / 3.8
        ra_logo.next_to(keyline, DOWN)

        title_text = Paragraph(
            title, **white_text_style, font_size=48, weight="BOLD", line_spacing=0.55
        ).to_corner(UP + LEFT)

        max_width = (ra_logo.get_left() - title_text.get_left())[0] - 0.7
        if title_text.width > max_width:
            title_text.scale_to_fit_width(max_width).next_to(
                title_text, DOWN, buff=0.3, aligned_edge=LEFT
            ).to_corner(UP + LEFT)
        author_text = (
            Text(author, **white_text_style, font_size=40)
            .scale(0.8)
            .next_to(title_text, DOWN, buff=0.3, aligned_edge=LEFT)
        )

        if author_text.width > max_width:
            author_text.scale_to_fit_width(max_width).next_to(
                title_text, DOWN, buff=0.3, aligned_edge=LEFT
            )

        venue_text = (
            Text(venue, **white_text_style, font_size=40)
            .scale(0.5)
            .next_to(ra_logo, RIGHT, aligned_edge=DOWN)
            .next_to(author_text, DOWN, aligned_edge=LEFT)
        )

        self.add(
            background.shift(DOWN * 0.7),
            title_bar,
            title_text,
            author_text,
            keyline,
            ra_logo,
            venue_text,
        )
