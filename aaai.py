from manim import *
from manim_slides import Slide
from manim_beamer import *

FRAME_WIDTH = config["frame_width"]
FRAME_HEIGHT = config["frame_height"]

hf = HeaderFooter(
    {
        "Background and Motivation": 3,
        "Proof Logging": 2,
        "Pseudo-Boolean Reasoning": 2,
        "How to Write Proofs": 3,
        "Conclusions": 3,
    },
    title="Proof Logging for Constraint Programming",
    name="Matthew McIlree",
)


class AAAITitle(TalkSlide):
    def construct(self):
        self.add(
            TitleSlide(
                "Proof Logging\nfor Constraint Programming",
                venue="AAAI, Philadelphia, Pennsylvania, 2 March 2025",
                author="Matthew McIlree and Ciaran McCreesh",
            )
        )
        self.wait()


class WhatIsCP(TalkSlide):
    def construct(self):
        hf.set_current(0, 0)
        self.add(hf)

        variables = VGroup(*[MathTex(v, color=BLACK) for v in ["X", "Y", "Z", "W"]])

        value_sets = [[1, 2, 3], [3, 4, 5], [2, 3, 4], [4, 5, 6]]
        values = VGroup(
            *[
                MathTex(v, color=BLACK)
                for v in [
                    "\{" + ", ".join([str(v) for v in vs]) + "\}" for vs in value_sets
                ]
            ]
        )

        variables.scale(1.7)
        values.scale(1.7)

        values.arrange(buff=0.6).shift(DOWN)
        for i in range(len(variables)):
            variables[i].next_to(values[i], UP, buff=1)

        self.add(variables, values)
        self.wait()

        cons = [
            [1, 3, 2, 4],
            [2, 4, 3, 6],
            [3, 5, 4, 6],
            [1, 4, 3, 5],
        ]
        anims = []

        for con_num in range(len(cons)):
            for set_num in range(len(cons[con_num])):
                for idx in range(3):
                    if value_sets[set_num][idx] == cons[con_num][set_num]:
                        anims.append(
                            Indicate(values[set_num][0][idx * 2 + 1], color=PURE_RED)
                        )
            self.play(*anims)
            anims = []


class CorrectnessMatters(TalkSlide):
    def construct(self):
        hf.set_current(0, 1)
        self.add(hf)
        self.wait()


class BugsInCPSolvers(TalkSlide):
    def construct(self):
        hf.set_current(0, 2)
        self.add(hf)
        self.wait()


class ProofLoggingIdea(TalkSlide):
    def construct(self):
        hf.set_current(1, 0)
        self.add(hf)
        self.wait()


class ProofSystemRequirements(TalkSlide):
    def construct(self):
        hf.set_current(1, 1)
        self.add(hf)
        self.wait()


class PseudoBooleanism(TalkSlide):
    def construct(self):
        hf.set_current(2, 0)
        self.add(hf)
        self.wait()


class ProofRules(TalkSlide):
    def construct(self):
        hf.set_current(2, 1)
        self.add(hf)
        self.wait()


class BacktrackingSearchProofPB(TalkSlide):
    def construct(self):
        hf.set_current(3, 0)
        self.add(hf)
        self.wait()


class BacktrackingSearchProofCP(TalkSlide):
    def construct(self):
        hf.set_current(3, 1)
        self.add(hf)
        self.wait()


class CPPropagatorJustifications(TalkSlide):
    def construct(self):
        hf.set_current(3, 2)
        self.add(hf)
        self.wait()


class TheChallenge(TalkSlide):
    def construct(self):
        hf.set_current(4, 0)
        self.add(hf)
        self.wait()


class ThisPaper(TalkSlide):
    def construct(self):
        hf.set_current(4, 1)
        self.add(hf)
        self.wait()


class Takeaways(TalkSlide):
    def construct(self):
        hf.set_current(4, 2)
        self.add(hf)
        self.wait()
