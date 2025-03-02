from manim import *
from manim_slides import Slide
from manim_beamer import *
from bounds_bar import BoundsBar

import os

FRAME_WIDTH = config["frame_width"]
FRAME_HEIGHT = config["frame_height"]

hf = HeaderFooter(
    {
        "Background and Motivation": 4,
        "Proof Logging": 3,
        "...for CP?": 4,
        "This Paper": 4,
    },
    title="Certifying Bounds Propagation for Integer Multiplication Constraints",
    name="Matthew McIlree",
)


class AAAITitle(TalkSlide):
    def construct(self):
        self.add(
            TitleSlide(
                "Certifying Bounds Propagation\nfor Integer Multiplication Constraints",
                venue="AAAI, Philadelphia, Pennsylvania, 2 March 2025",
                author="Matthew McIlree and Ciaran McCreesh",
            )
        )
        self.wait()


class CorrectAnswers(TalkSlide):
    def construct(self):
        hf.set_current(0, 0)
        self.add(hf)
        text = Text('CP Solvers are "Exact"', **TALK_BODY_TEXT).scale(2)
        self.add(text)
        self.next_slide()
        num_bugs = 5
        bug_size = 0.1
        bug_rots = [(i + 1) * 0.377 * PI for i in range(num_bugs)]
        bugs = Group(
            *[
                ImageMobject("img/bug.png").scale(bug_size).rotate(bug_rots[i])
                for i in range(num_bugs)
            ]
        ).arrange(buff=0.5)

        final_pos = {str(bug): bug.get_center() for bug in bugs}

        for i, bug in enumerate(bugs):
            bug.shift(
                rotate_vector(bug.get_top() - bug.get_center(), bug_rots[i]) * -10
            )

        self.add(bugs)

        self.wait()

        self.next_slide()

        self.play(
            *[
                bug.animate.shift(
                    rotate_vector(bug.get_top() - bug.get_center(), bug_rots[i]) * 10
                )
                for i, bug in enumerate(bugs)
            ],
            run_time=3,
        )

        self.next_slide()


class CorrectnessMatters(TalkSlide):
    def construct(self):
        self.next_slide(
            notes="""
            """,
        )
        hf.set_current(0, 1)
        self.add(hf)
        # self.add(SlideTitle("Correctness Matters!").set_x(0))

        self.play(
            FadeIn(ImageMobject("./img/applications.png").shift(DOWN * 0.1).scale(0.37))
        )
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
        - Formal verification: far away from being able to deal with CP
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
        hf.set_current(1, 2)
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


class EncodingProblems(TalkSlide):
    def construct(self):
        hf.set_current(2, 0)
        title = SlideTitle("Pseudo-Boolean Proof Logging for CP")
        self.add(hf)
        self.add(title)
        line = Line(UP * 2, DOWN * 3, color=GRAY)
        self.add(line)
        self.wait()
        self.next_slide()

        cp_vars = (
            Group(*[MathTex(s, color=BLACK) for s in ["X", "Y", "Z"]])
            .scale(2.5)
            .arrange(buff=0.8)
            .move_to(LEFT * FRAME_WIDTH / 4 + UP * 0.4)
        )

        pb_vars = [
            VGroup(
                *[MathTex(v + r"_{b" + str(i) + r"}", color=BLACK) for i in range(3)]
            )
            for v in ["x", "y", "z"]
        ]

        self.play(*[FadeIn(var) for var in cp_vars])

        self.next_slide()

        for i in range(len(pb_vars)):
            pb_vars[i].arrange(buff=0.8).move_to(
                RIGHT * FRAME_WIDTH / 4 + UP * FRAME_HEIGHT / 6
            )

            if i > 0:
                pb_vars[i].next_to(pb_vars[i - 1], DOWN, buff=0.6)

            rect = SurroundingRectangle(
                pb_vars[i], color=UG_COBALT, corner_radius=0.05, buff=0.15
            )

            self.play(Transform(cp_vars[i].copy(), pb_vars[i]), Create(rect))

        self.next_slide()

        eq_con = (
            MathTex(r"X = Y", color=BLACK).scale(2).next_to(cp_vars, DOWN, buff=1.5)
        )

        self.play(FadeIn(eq_con))

        self.next_slide()

        pb_con = (
            MathTex(
                r"x_{b0} + 2 x_{b1} + 4 x_{b2} - y_{b0} - 2 y_{b1} - 4 y_{b2} \geq 0\\ -x_{b0} - 2 x_{b1} - 4 x_{b2} + y_{b0} + 2 y_{b1} + 4 y_{b2} \geq 0",
                color=BLACK,
            )
            .scale(0.7)
            .next_to(pb_vars[2], DOWN, buff=1)
        )

        self.play(Transform(eq_con.copy(), pb_con))
        self.wait()


class PrintStatements(TalkSlide):
    def construct(self):
        hf.set_current(2, 1)
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


class ProofLoggingInvariant(TalkSlide):
    def construct(self):
        hf.set_current(2, 2)
        self.add(hf)
        self.add(SlideTitle("Proof Logging Invariant"))

        invariant = (
            MathTex(
                r"\textit{reason}", r"\implies", r"\textit{conclusion}", color=BLACK
            )
            .scale(2)
            .move_to(UP * FRAME_HEIGHT / 6)
        )
        self.play(Write(invariant))
        self.next_slide()

        invariant_ex = (
            MathTex(
                r"x_{=1}",
                r"\land",
                r"y_{=2}",
                r"\implies",
                r"\lnot",
                r"z_{=4}",
                r"\land",
                r"\lnot",
                r"w_{=5}",
                color=BLACK,
            )
            .scale(2)
            .next_to(invariant, DOWN, buff=0.8)
        )
        self.play(TransformMatchingTex(invariant.copy(), invariant_ex))
        self.next_slide()
        invariant_pb = (
            MathTex(
                r"-" r"x_{=1}",
                r"-",
                r"y_{=2}",
                r"",
                r"-",
                r"z_{=4}",
                r"-",
                r"w_{=5}",
                r"\geq -2",
                color=UG_BLUE,
            )
            .scale(2)
            .next_to(invariant_ex, DOWN, buff=0.8)
        )

        self.play(TransformMatchingTex(invariant_ex.copy(), invariant_pb))


class TheChallenge(TalkSlide):
    def construct(self):
        hf.set_current(2, 3)

        big_list = (
            Group(
                *[MathTex(b, color=BLACK) for b in big_constraints_list],
                z_index=hf.z_index - 1,
            )
            .arrange(DOWN)
            .align_to([0, 0, 0], UP)
        )

        self.bring_to_back(big_list)
        con_count = 0

        self.add(big_list)
        self.add(hf)
        self.play(
            big_list.animate.shift(-big_list.get_bottom()),
            rate_func=rate_functions.linear,
            run_time=25,
        )


class ThisPaper(TalkSlide):
    def construct(self):
        hf.set_current(3, 0)
        self.add(SlideTitle("This Paper:"))
        paper = ImageMobject("./img/paper.png").scale(0.7).shift(DOWN * 0.8 + LEFT * 3)
        paper.set_z_index(-1)

        mult = MathTex(r"X \times Y = Z", color=BLACK).scale(1.5).shift(RIGHT * 4)

        self.add(hf)

        self.play(FadeIn(paper, shift=UP))

        self.next_slide()

        self.play(FadeIn(mult))

        self.next_slide()

        rect = SurroundingRectangle(mult, corner_radius=0.1, color=PURE_RED, buff=0.4)

        mult_grp = Group(mult, rect)

        self.play(
            FadeOut(paper),
            FadeIn(rect),
            mult_grp.animate.move_to([0, 0, 0]).shift(UP * 1.5),
        )
        self.next_slide()

        pb_enc = (
            MathTex(
                r"\sum_i 2 i z_{bi} - \sum_i \sum_j 2^{i+j} {{xy_{bij}}} = 0",
                color=BLACK,
            )
            .next_to(mult_grp, DOWN, buff=1)
            .shift(LEFT * 0.3)
        )

        self.play(Transform(mult.copy(), pb_enc))

        self.next_slide()

        bit_vars = MathTex(
            r"{{xy_{bij}}} \iff x_{bi} + y_{bj} \geq 2", color=BLACK
        ).next_to(pb_enc, DOWN, buff=0.8)

        self.play(
            Transform(
                pb_enc.copy()[1],
                bit_vars,
            )
        )


class BoundsConsistency(TalkSlide):
    def construct(self):
        hf.set_current(3, 1)
        self.add(hf)
        self.add(SlideTitle("Bounds Consistency"))
        self.add(hf)
        x_bar = BoundsBar(
            var_name="X", max_bounds=(-2, 7), bounds=[(-2, 7), (-2, 7), (-2, 7)]
        ).next_to(hf.h_background2, DOWN, buff=1)

        y_bar = BoundsBar(
            var_name="Y", max_bounds=(-2, 7), bounds=[(-2, 7), (-2, 7), (-2, 7)]
        ).next_to(x_bar, DOWN, buff=0.8)

        z_bar = BoundsBar(
            var_name="Z", max_bounds=(-2, 7), bounds=[(-2, 7), (-2, 7), (-2, 7)]
        ).next_to(y_bar, DOWN, buff=0.8)

        self.add(x_bar, y_bar, z_bar)
        self.wait()

        self.next_slide()

        self.play(x_bar.animate.update_bounds([(-2, 7), (2, 3), (2, 3)]))
        self.play(y_bar.animate.update_bounds([(-2, 7), (1, 2), (1, 2)]))
        self.play(z_bar.animate.update_bounds([(-2, 7), (-1, 7), (-1, 7)]))
        self.next_slide()

        self.play(z_bar.animate.update_bounds([(-2, 7), (-1, 7), (2, 6)]))

        self.next_slide()

        new_x_bar = BoundsBar(
            var_name="X", max_bounds=(-6, 5), bounds=[(-6, 5), (-6, 5), (-6, 5)]
        ).move_to(x_bar)

        new_y_bar = BoundsBar(
            var_name="Y", max_bounds=(-6, 5), bounds=[(-6, 5), (-1, 2), (-1, 2)]
        ).move_to(y_bar)

        new_z_bar = BoundsBar(
            var_name="Z",
            max_bounds=(-6, 5),
            bounds=[(-6, 5), (-4, -1), (-4, -1)],
        ).move_to(z_bar)

        self.play(
            x_bar.animate.become(new_x_bar),
            y_bar.animate.become(new_y_bar),
            z_bar.animate.become(new_z_bar),
        )

        self.remove(x_bar)
        self.next_slide()

        self.play(new_x_bar.animate.update_bounds([(-6, 5), (-6, 5), (-4, 5)]))

        self.next_slide()

        self.play(new_x_bar.animate.update_bounds([(-6, 5), (-6, 5), (-4, 4)]))


class Overheads(TalkSlide):
    def construct(self):
        hf.set_current(3, 2)
        self.add(hf)

        self.add(SlideTitle("Overheads"))
        l_graph = ImageMobject("img/experiments1.png").scale(0.3)
        r_graph = ImageMobject("img/experiments2.png").scale(0.3)

        self.add(Group(l_graph, r_graph).arrange().shift(DOWN * 0.3))

        self.wait()


class Takeaways(TalkSlide):
    def construct(self):
        hf.set_current(3, 3)
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
