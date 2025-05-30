def propagate(state):
    # Run propagators
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