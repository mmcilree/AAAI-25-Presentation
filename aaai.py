from manim import *
from manim_slides import Slide
from manim_beamer import *

import os

FRAME_WIDTH = config["frame_width"]
FRAME_HEIGHT = config["frame_height"]

hf = HeaderFooter(
    {
        "Background and Motivation": 4,
        "Proof Logging": 2,
        "Pseudo-Boolean Reasoning": 4,
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
        self.next_slide(
            notes="""
**Constraint Programming:**
- Most people should be familiar
- Variables, Values, Constraints
- Asking: satisfy or optimise
- Model rostering, scheduling, resource allocation, 
- CP solvers can tackle industrial size instances with hundreds or even thousands of variables and constraints
""",
        )
        hf.set_current(0, 0)
        self.add(hf)

        variables = VGroup(*[MathTex(v, color=BLACK) for v in ["X", "Y", "Z", "W"]])

        value_sets = [[1, 2, 3], [3, 4, 5], [2, 3, 4], [4, 5, 6]]
        values = VGroup(
            *[
                MathTex(v, color=BLACK)
                for v in [
                    r"\{" + ", ".join([str(v) for v in vs]) + r"\}" for vs in value_sets
                ]
            ]
        )

        variables.scale(1.7)
        values.scale(1.7)

        values.arrange(buff=0.6).shift(DOWN)
        for i in range(len(variables)):
            variables[i].next_to(values[i], UP, buff=1)

        self.next_slide()
        self.play(Create(variables))

        self.next_slide()

        self.play(Create(values))

        self.next_slide()

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
                    self.next_slide()
            self.play(*anims)
            anims = []


class CorrectnessMatters(TalkSlide):
    def construct(self):
        self.next_slide(
            notes="""
    **Correctness matters:**
    - In some problems, correctness matters
    - Should be fairly self explanatory
    - Safety, Legal, Ethical or Financial
    - Mildly bad to disatrous consequences
    """,
        )
        hf.set_current(0, 1)
        self.add(hf)
        self.add(SlideTitle("Correctness Matters!").set_x(0))
        self.add(ImageMobject("./img/applications.png").scale(0.32).shift(DOWN * 0.5))
        self.wait()


class BugsInCPSolvers(TalkSlide):
    def construct(self):
        self.next_slide(
            notes="""
        - CP Solvers have bugs
        - All software has bugs
        - Sometimes that leads to the solver getting the wrong answer
        - Asked for evidence
        - Wrong solutions
        - False claim of optimality
        - False claim of unsatisfiability
        """,
        )
        hf.set_current(0, 2)
        self.add(hf)
        bug_imgs = []
        dir = sorted(os.listdir("./img/bugs"))
        for i, file in enumerate(dir):
            bug_imgs.append(
                Group(ImageMobject(os.path.join("./img/bugs/", file))).scale(
                    0.7 + 0.001 * i
                )
            )

        Group(*bug_imgs)
        self.play(FadeIn(bug_imgs[0], shift=RIGHT))
        for i in range(len(bug_imgs) - 1):
            self.next_slide()
            self.play(
                FadeOut(bug_imgs[i], shift=RIGHT), FadeIn(bug_imgs[i + 1], shift=RIGHT)
            )
            self.remove(bug_imgs[i])

        self.next_slide()


class Testing(TalkSlide):
    def construct(self):
        self.next_slide(
            notes="""
        - Testing: important, but will never demonstrate the absence of bugs
        - Formal verification:
        """,
        )
        hf.set_current(0, 3)
        self.add(hf)

        testing_img = Group(ImageMobject("./img/Testing.png"))
        self.play(FadeIn(testing_img))
        prev_height = testing_img.height
        self.next_slide()

        self.play(testing_img.animate.move_to(LEFT * 4.5).scale(0.8).fade(0.4))

        formal_verif_img = (
            ImageMobject("./img/FormalVerif.png")
            .scale_to_fit_height(prev_height)
            .shift(RIGHT * 0.5)
        )

        self.next_slide()

        self.play(FadeIn(formal_verif_img))

        self.next_slide()

        self.play(
            formal_verif_img.animate.move_to(RIGHT * 4.5).scale(0.8).set_opacity(0.4)
        )

        self.next_slide()

        qmark = Text("?", color=BLACK).scale(9)

        self.play(FadeIn(qmark))
        self.wait()


class ProofLoggingIdea(TalkSlide):
    def construct(self):
        hf.set_current(1, 0)
        self.add(hf)
        title = SlideTitle("Proof Logging (the basic idea)")
        self.add(title)
        self.add(hf)
        proof_diagram = ProofDiagram()
        self.wait()
        while proof_diagram.has_next():
            self.next_slide()
            self.play(proof_diagram.next_anim())

        proof = proof_diagram.proof

        self.next_slide(auto_next=True)

        self.play(
            FadeOut(title),
            *[FadeOut(m) for m in proof_diagram if m != proof],
            proof.animate.set_width(4.8).set_height(5.8).move_to([0, 0, 0]),
            hf.animate.next(),
        )


class ProofSystemRequirements(TalkSlide):
    def construct(self):
        hf.set_current(1, 1)
        self.add(hf)
        proof = ProofScroll().move_to([0, 0, 0])
        proof.width = 4.8
        proof.height = 5.8

        self.add(proof)
        self.wait()
        self.next_slide()
        self.play(FadeOut(proof.header), FadeOut(proof.lines))

        self.next_slide()
        derivations = Group(
            *[
                Text(f"Derivation {i} (Rule)", **TALK_BODY_TEXT).scale(0.7)
                for i in range(1, 7)
            ],
            Text("Conclusion □", **TALK_BODY_TEXT),
        )

        derivations.arrange(DOWN).next_to(proof.scroll.get_body_top(), DOWN)

        self.play(LaggedStart(*[FadeIn(d) for d in derivations[:-1]], lag_ratio=0.5))

        self.next_slide()
        self.play(FadeIn(derivations[-1]))

        self.next_slide()

        math_derivations = MathTex(
            r"""
            3x + 2y + z &\geq 1 \;\text{(RUP)}\\
            2y + 4\bar{z} &\geq 5 \;\text{(Add.)}\\
            w \iff 3\bar{x} + 8y + w &\geq 3 \;\text{(Red.)}\\
            2y + w + 2\bar{z} &\geq 2 \;\text{(RUP)}\\
            x + \bar{y} + 2z &\geq 1 \;\text{(RUP)}\\
            3x + 2y + \bar{z} + w &\geq 5 \;\text{(RUP)}\\
                0 &\geq 1 \;\text{(RUP)}
            """,
            color=BLACK,
            font_size=48,
        ).next_to(proof.scroll.get_body_top(), DOWN)

        wider_scroll = Scroll(
            width=proof.scroll.width * 1.4,
            height=proof.scroll.height * 0.95,
            tube_height=0.3,
        ).shift(DOWN * 0.2)
        self.play(
            FadeOut(derivations),
            FadeIn(math_derivations, scale=0.5),
            proof.scroll.animate.become(wider_scroll),
        )


class VeriPB(TalkSlide):
    def construct(self):
        hf.set_current(2, 0)
        self.add(hf)
        veripb = Text(
            "VeriPB",
            font=CMU_SANS,
            color=BLACK,
            font_size=90,
            weight=BOLD,
        )

        pb = Text("Pseudo-Boolean\nProof Language", **TALK_BODY_TEXT).move_to(
            UP * 2 + LEFT * 4
        )
        cutting_planes = Text(
            "Cutting Planes + \nAdditional Rules", **TALK_BODY_TEXT
        ).move_to(DOWN * 2 + LEFT * 4)
        working_checker = Text(
            "Working proof\nchecker implementation", **TALK_BODY_TEXT
        ).move_to(UP * 2 + RIGHT * 4)
        multiple_paradigms = (
            BulletPoints("SAT", "MaxSAT", "PB", "Graphs", "...CP!", **TALK_BODY_TEXT)
            .scale(0.8)
            .move_to(RIGHT * 5 + DOWN)
        )
        self.add(veripb)
        self.next_slide()

        for t in [pb, cutting_planes, working_checker, multiple_paradigms]:
            self.play(FadeIn(t))
            self.next_slide()

        self.next_slide()

        wing1 = (
            ImageMobject("./img/angel_wing1.png")
            .scale(0.5)
            .next_to(veripb, LEFT, buff=-0.1)
        )

        wing2 = (
            ImageMobject("./img/angel_wing2.png")
            .scale(0.5)
            .next_to(veripb, RIGHT, buff=-0.1)
        )

        halo_band = Ellipse(width=1.3, height=0.4, color=YELLOW, stroke_width=10)
        halo_outline = Ellipse(width=1.3, height=0.4, color=BLACK, stroke_width=16)
        halo = Group(halo_outline, halo_band)
        halo.rotate(PI / 80)
        halo.move_to(veripb.get_top() + UP * 0.4)
        self.play(FadeIn(wing1), FadeIn(wing2), FadeIn(halo))

        self.next_slide(auto_next=True)
        new_title = SlideTitle("Pseudo-Boolean Constraints")
        self.play(
            *[
                FadeOut(t)
                for t in [
                    wing1,
                    wing2,
                    halo,
                    veripb,
                    cutting_planes,
                    working_checker,
                    multiple_paradigms,
                ]
            ],
            Transform(pb, new_title),
            hf.animate.next(),
        )

        self.wait()


class PseudoBooleanism(TalkSlide):
    def construct(self):
        hf.set_current(2, 1)
        self.add(hf)
        self.add(SlideTitle("Pseudo-Boolean Constraints"))

        self.next_slide()

        sum_x = MathTex(r"\sum_{i=0}^{n-1} {{a_i}} {{x_i}} \geq {{A}}", color=BLACK)
        sum_x.scale(2.4).shift(UP * 0.25)
        sum_x_copy = sum_x.copy()
        sum_x_copy.set_opacity(0)
        sum_x_copy[1].set_opacity(1)
        sum_x_copy[5].set_opacity(1)

        self.play(FadeIn(sum_x))

        self.next_slide()

        int_def = MathTex(r"{{a_i}}, {{A}} \in \mathbb Z", color=BLACK)
        lit_def = MathTex(
            r"{{\ell_i}} \in \{x_i, \overline{x} = 1 - x_i\}", color=BLACK
        )

        defs = Group(lit_def, int_def).scale(1.5).arrange(buff=1.5)
        defs.next_to(sum_x, DOWN, buff=0.75)

        self.play(TransformMatchingTex(sum_x_copy, int_def))

        self.next_slide()

        sum_l = MathTex(r"\sum_{i=0}^{n-1} {{a_i}} {{\ell_i}} \geq {{A}}", color=BLACK)
        sum_l.scale(2.4).shift(UP * 0.25)

        self.play(TransformMatchingTex(sum_x, sum_l))

        self.next_slide()

        sum_l_copy = sum_l.copy()
        sum_l_copy.set_opacity(0)
        sum_l_copy[2].set_opacity(1)

        self.play(TransformMatchingTex(sum_l_copy, lit_def))
        self.wait()


class ProofRules(TalkSlide):
    def construct(self):
        hf.set_current(2, 2)
        self.add(hf)
        litaxiom = MathTex(r"\quad \frac{\phantom{\Sigma}}{\ell_i \geq 0}", color=BLACK)

        addition = MathTex(
            r"\frac{\sum a_i \ell_i \geq A \qquad \sum b_i \ell'_i \geq B}{\sum a_i\ell_i + \sum b_i\ell'_i \geq A + B}",
            color=BLACK,
        )
        multiplication = MathTex(
            r"\frac{\sum a_i \ell_i \geq A}{\quad \lambda a_i \ell_i \geq \lambda A}, \; \lambda \in \mathbb{N}^+",
            color=BLACK,
        )

        division = MathTex(
            r"\frac{\sum a_i \ell_i \geq A}{\sum \lceil a_i/c \rceil \ell_i  \geq \lceil A/c \rceil}, \; c \in \mathbb{N}^+",
            color=BLACK,
        )

        rules = (
            Group(litaxiom, addition, multiplication, division)
            .arrange_in_grid(buff=(1.2, 1.6))
            .shift(DOWN * 0.7)
        )

        litaxiom.shift(DOWN * 0.25)

        titles = Group(
            *[
                Text(s, **TALK_BODY_TEXT)
                for s in [
                    "Literal Axiom:",
                    "Addition:",
                    "Scalar Multiplication:",
                    "Division:",
                ]
            ]
        )

        for t, r in zip(titles, rules):
            t.next_to(r, UP)

        titles[0].align_to(titles[1], UP)
        titles[2].align_to(titles[3], UP)

        title = SlideTitle("Cutting Planes Rules: ")
        self.play(FadeIn(title))
        self.next_slide()

        self.play(FadeIn(rules, titles))
        self.wait()
        self.next_slide(auto_next=True)
        new_title = SlideTitle("Additional Rules:")
        self.play(
            Transform(title, new_title),
            hf.animate.next(),
            FadeOut(rules),
            FadeOut(titles),
        )


class AdditionalRules(TalkSlide):
    def construct(self):
        hf.set_current(2, 3)
        self.add(hf)
        title = SlideTitle("Additional Rules:")
        self.add(title)
        self.wait()
        self.next_slide()

        rup = (
            MarkupText(
                r'<b>RUP</b> := "Sufficiently obvious for the verifier."',
                **TALK_BODY_TEXT,
            )
            .next_to(title, DOWN, buff=1)
            .align_to(title, LEFT)
        )

        red = (
            MarkupText(
                r'<b>RED</b> := "Allowed to define new variables."',
                **TALK_BODY_TEXT,
            )
            .scale(1)
            .next_to(rup, DOWN, buff=1)
            .align_to(rup, LEFT)
        )

        self.play(FadeIn(rup))
        self.next_slide()
        self.play(FadeIn(red), shift=DOWN)


class PrintStatements(TalkSlide):
    def construct(self):
        hf.set_current(3, 0)
        self.add(hf)
        # Define the initial function code (without print statements)
        code_initial = """
def propagate(state):
    pass

def run_solver(state):
    if propagate(state):
        branch_var = choose_branch_var(state)
        if branch_var is None:
            return True
        else:
            for value in state.get_domain(branch_var):
                new_state = state.clone()
                new_state.guess(branch_var, value)
                run_solver(new_state)
            return False

    return False
        """.strip()

        # Define the modified function lines (with print statements added gradually)
        code_modified = """
def propagate(state):
    print(justify_propagation_str(state))
    pass

def run_solver(state):
    if propagate(state):
        branch_var = choose_branch_var(state)
        if branch_var is None:
            print(log_sol_str(state))
            return True
        else:
            for value in state.get_domain(branch_var):
                new_state = state.clone()
                new_state.guess(branch_var, value)
                run_solver(new_state)
                print(justify_backtrack_str(state))
            return False

    return False
        """.strip()

        # Create Manim Code object for the initial state
        code_display = Code(
            code_string=code_initial,
            language="Python",
            background="window",
        ).scale(0.7)

        # Display the initial code block
        self.play(Write(code_display))
        self.wait(2)

        self.next_slide()

        new_code_display = (
            Code(
                code_string=code_modified,
                language="Python",
                background="window",
            )
            .scale(0.7)
            .align_to(code_display, UP)
        )
        self.play(
            TransformAddingLinesToCode(
                code_display, code_initial, new_code_display, code_modified
            )
        )
        code_display = new_code_display
        self.wait(1)


# class BacktrackingSearchProofPB(TalkSlide):
#     def construct(self):
#         hf.set_current(3, 0)
#         self.add(hf)
#         self.wait()


class Reification(TalkSlide):
    def construct(self):
        hf.set_current(3, 1)
        self.add(hf)
        var = MathTex(r"x_{i = j}", color=BLACK).scale(3)

        reified = (
            MathTex(
                r"x_{i = j}",
                r"\iff",
                r"x_{i \geq j} + x_{i \leq j} \geq 2",
                color=BLACK,
            )
            .scale(1.5)
            .shift(UP)
        )

        geq = (
            MathTex(
                r"x_{i \geq j}",
                r"\iff",
                r"x_{b0} + 2x_{b1} + 4x_{b2} \geq j",
                color=BLACK,
            )
            .scale(1.5)
            .next_to(reified, DOWN)
        )

        leq = (
            MathTex(
                r"x_{i \leq j}",
                r"\iff",
                r"-x_{b0} - 2x_{b1} - 4x_{b2} \geq -j",
                color=BLACK,
            )
            .scale(1.5)
            .next_to(geq, DOWN)
        )

        reified_split1 = (
            MathTex(
                r"2 \bar " + "x_{i = j}",
                "+",
                r"x_{i \geq j} + x_{i \leq j} \geq 2",
                color=BLACK,
            )
            .scale(1.5)
            .shift(UP)
        )

        reified_split2 = (
            MathTex(
                r"x_{i = j}",
                "+",
                r"\bar x_{i \geq j} + \bar x_{i \leq j} \geq 1",
                color=BLACK,
            )
            .scale(1.5)
            .shift(UP)
        ).next_to(reified_split1, DOWN)

        self.add(var)
        self.next_slide(notes="Hello these are some notes")
        self.play(TransformMatchingTex(var, reified))
        self.next_slide()
        self.play(FadeIn(geq, shift=DOWN), FadeIn(leq, shift=DOWN))
        self.next_slide()

        self.play(
            TransformMatchingTex(reified, reified_split1),
            FadeIn(reified_split2, shift=DOWN),
            FadeOut(geq),
            FadeOut(leq),
        )

        self.next_slide()

        self.play(reified_split1[0][0].animate.set_color(PURE_RED).scale(1.3))


class BacktrackingSearchProofCP(TalkSlide):
    def construct(self):
        hf.set_current(3, 2)
        self.add(hf)
        title = SlideTitle("CP Proof Logging Framework")
        self.add(hf)
        self.add(title)

        vars = Group(
            *[MathTex(f"X_{i}", color=BLACK) for i in range(0, 3)],
            MathTex("X_4", opacity=1),
        )

        vars.arrange(DOWN + LEFT * 0.7, buff=0.7)

        contr = Text("×", color=PURE_RED, weight=BOLD).move_to(vars[3].get_center())

        guess_arrows = VGroup(
            *[
                Arrow(
                    vars[i],
                    vars[i + 1],
                    stroke_color=UG_BLUE,
                    stroke_width=5,
                    buff=0.15,
                )
                for i in range(0, 3)
            ]
        )

        guess_labels = VGroup(
            *[
                MathTex(" = 0 ", color=BLACK)
                .move_to(guess_arrows.submobjects[i])
                .scale(0.5)
                .shift(RIGHT * 0.4)
                for i in range(0, 3)
            ]
        )

        backtrack_diagram = Group(vars[:-1], guess_arrows, guess_labels, contr)
        backtrack_diagram.shift(LEFT * 4)

        backtrack_just_title = (
            Text("Backtracking Justifications: ", **TALK_BODY_TEXT)
            .scale(0.7)
            .shift(RIGHT * 4 + UP * 1.5)
        )

        backtrack_just_title.color = UG_COBALT

        prop_just_title = (
            Text("Propagation Justifications: ", **TALK_BODY_TEXT)
            .scale(0.7)
            .next_to(backtrack_just_title, DOWN * 8)
        )

        prop_just_title.color = UG_COBALT
        self.wait()
        self.next_slide()
        self.play(FadeIn(backtrack_just_title))
        self.next_slide()
        self.play(FadeIn(prop_just_title))
        self.next_slide()

        for i in range(0, 3):
            self.play(
                FadeIn(vars[i]),
                GrowArrow(guess_arrows[i]),
                FadeIn(guess_labels[i]),
                run_time=0.5,
            )
            self.next_slide()

        self.play(FadeIn(contr))
        self.next_slide()

        backtrack_just = MathTex(
            r"\overline{x_{0 = 0}} + \overline{x_{1 = 0}} + \overline{x_{2 = 0}} \geq 1",
            color=BLACK,
        ).next_to(backtrack_just_title, DOWN * 2)

        prop_just = MathTex(
            r"{x_{0 = 0} \land x_{1 = 0} \implies \overline{x_{2 = 3} \geq 1",
            color=BLACK,
        ).next_to(prop_just_title, DOWN * 2)

        output_arrow2 = Arrow(
            prop_just.get_left() + LEFT * 2,
            prop_just.get_left(),
            tip_shape=StealthTip,
            color=GRAY,
            stroke_width=4,
        )

        output_arrow1 = Arrow(
            backtrack_just.get_left() + LEFT * 2,
            backtrack_just.get_left(),
            tip_shape=StealthTip,
            color=GRAY,
            stroke_width=4,
        ).align_to(output_arrow2, LEFT)

        self.play(
            FadeIn(backtrack_just, shift=RIGHT), FadeIn(output_arrow1, shift=RIGHT)
        )

        self.next_slide()

        self.play(FadeOut(contr), FadeOut(guess_labels[2]), FadeOut(guess_arrows[2]))

        self.next_slide()

        prop_arrow = DashedLine(
            vars[2].get_center(),
            vars[2].get_center() + RIGHT * 2.5,
            dash_length=0.1,
            color=UG_COBALT,
            buff=0.5,
        ).add_tip(
            tip_length=guess_arrows[0].tip.length, tip_width=guess_arrows[0].tip.width
        )

        prop = (
            MathTex(r" \neq 3 ", color=UG_COBALT).scale(0.7).next_to(prop_arrow, RIGHT)
        )

        self.play(
            GrowFromPoint(prop_arrow, prop_arrow.start), FadeIn(prop, shift=RIGHT)
        )

        self.next_slide()

        self.play(FadeIn(prop_just, shift=RIGHT), FadeIn(output_arrow2, shift=RIGHT))


# class TheChallenge(TalkSlide):
#     def construct(self):
#         hf.set_current(4, 0)
#         globals = ImageMobject("./img/globals.png").scale(3).align_on_border(UP, 3)
#         self.add(globals)
#         self.add(hf)
#         self.play(globals.animate.shift(UP * globals.height), run_time=15)


class ThisPaper(TalkSlide):
    def construct(self):
        hf.set_current(4, 1)
        self.add(SlideTitle("This Paper:"))
        paper = ImageMobject("./img/paper.png").scale(0.7).shift(DOWN * 0.8 + LEFT * 3)
        paper.set_z_index(-1)

        mult = MathTex(r"X \times Y = Z", color=BLACK).scale(1.5).shift(RIGHT * 4)

        self.add(hf)

        self.play(FadeIn(paper, shift=UP))

        self.next_slide()

        self.play(FadeIn(mult))

        self.next_slide()

        bnds1 = (
            MathTex(r"\geq 7 \qquad \geq 3 \qquad \geq \; ?", color=PURE_RED)
            .scale(0.9)
            .next_to(mult, UP)
            .align_to(mult, LEFT)
        )
        bnds2 = (
            MathTex(r"\geq \; ? \qquad \geq -3 \quad \geq -4", color=PURE_RED)
            .scale(0.9)
            .next_to(mult, DOWN)
            .align_to(mult, LEFT)
        )
        self.next_slide()

        self.play(FadeIn(bnds1, shift=UP))

        self.next_slide()

        self.play(FadeIn(bnds2, shift=DOWN))

        self.next_slide()

        pb_enc = (
            MathTex(
                r"\sum_i 2 i z_{bi} - \sum_i \sum_j 2^{i+j} xy_{bij} = 0", color=BLACK
            )
            .scale(0.8)
            .next_to(bnds2, DOWN, buff=0.8)
            .shift(LEFT * 0.3)
        )

        self.play(FadeIn(pb_enc, shift=DOWN))


class Takeaways(TalkSlide):
    def construct(self):
        hf.set_current(4, 2)
        self.add(hf)
        title = SlideTitle("If nothing else:")
        self.add(title)
        bullets = (
            BulletPoints(
                "Proof logging is a thing worth doing!",
                "Proof logging can be applied to CP via (effectively) print statements.",
                "Pseudo-Boolean (0-1 ILP) proofs can be applied without\nthe solver doing any PB reasoning.",
                "In particular, bounds-consistent multiplication, which seems awkard,\nis doable with VeriPB proofs :-)",
                "Interested in the implementation?:\nhttps://github.com/ciaranm/glasgow-constraint-solver",
                **TALK_BODY_TEXT,
            )
            .shift(DOWN * 0.5)
            .scale(0.7)
            .align_to(title, LEFT)
        )
        self.next_slide()

        for b in bullets.bullet_texts:
            self.play(Write(b))
            self.next_slide()

        self.wait()
