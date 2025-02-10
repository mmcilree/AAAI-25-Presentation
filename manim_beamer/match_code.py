from manim import *
from manim.animation.transform_matching_parts import TransformMatchingAbstractBase


class TransformAddingLinesToCode(LaggedStart):

    def __init__(
        self,
        code: Code,
        code_str: str,
        target: Code,
        target_str: str,
        **kwargs,
    ):
        anims = []
        write_anims = []
        anims.append(Transform(code.background, target.background, **kwargs))
        for i in range(len(target.line_numbers)):
            if i < len(code.line_numbers):
                anims.append(Transform(code.line_numbers[i], target.line_numbers[i]))
            else:
                anims.append(FadeIn(target.line_numbers[i], shift=DOWN))

        code_str_lines = code_str.split("\n")
        target_str_lines = target_str.split("\n")

        j = 0
        for i in range(len(target.code_lines.lines[0])):
            if target_str_lines[i] == code_str_lines[j]:
                anims.append(
                    Transform(code.code_lines[j], target.code_lines[i], **kwargs)
                )
                j += 1
            else:
                write_anims.append(Write(target.code_lines[i], **kwargs))
        group1 = AnimationGroup(*anims)
        group2 = AnimationGroup(*write_anims)
        super().__init__(group1, group2, lag_ratio=0.5)


if __name__ == "__main__":
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
    print("Added Line")
    pass

def run_solver(state):
    if propagate(state):
        branch_var = choose_branch_var(state)
        if branch_var is None:
            return True
        else:
            for value in state.get_domain(branch_var):
            print("Added Line")
                new_state = state.clone()
                new_state.guess(branch_var, value)
                run_solver(new_state)
            return False

return False
        """.strip()

    code_display = Code(
        code_string=code_initial,
        language="Python",
    )

    new_code_display = Code(
        code_string=code_modified,
        language="Python",
    ).align_to(code_display, UP)

    anims = TransformMatchingCode(code_display, new_code_display)
