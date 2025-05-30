def propagate(state):
    # Run propagators
    pass
def run_solver(state):
    if propagate(state):
        branch_var = choose_branch_var(state)
        if branch_var is None:
            self.proof.log_solution(state.assigned_vars, state)
            self.proof.justify_backtrack(state)
            return True # Stop looking
        else:
            for value in state.get_domain(branch_var):
                new_state = state.clone()
                # guess branch_var == value
                self.proof.log_guess(branch_var, value)
                new_state.guess(branch_var, value)
                run_solver(new_state)
            self.proof.justify_backtrack(state)
            return False
    
    self.proof.justify_backtrack(state)

    return False