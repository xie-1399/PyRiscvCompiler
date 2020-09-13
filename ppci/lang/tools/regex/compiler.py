from .parser import parse
from .regex import NULL
from ....utils.integer_set import IntegerSet


def compile(r: str):
    """ Turn regular expression into a DFA """
    expr = parse(r)

    states = {expr: 0}
    transitions = [[]]
    stack = [expr]

    while stack:
        state = stack.pop()
        state_number = states[state]
        print("=> state", state_number, ":", state, type(state))
        for derivative_class in state.derivative_classes():

            assert isinstance(derivative_class, IntegerSet)
            print("  -> derivative_class", derivative_class)

            if not derivative_class:
                continue

            # First symbol in this class:
            symbol = derivative_class.ranges[0][0]

            # Determine next state for this symbol class:
            next_state = state.derivative(symbol)

            # Add state if not yet present:
            if next_state not in states:
                states[next_state] = len(states)
                transitions.append([])
                stack.append(next_state)

            # Add transitions to next state:
            next_state_number = states[next_state]
            for first, last in derivative_class.ranges:
                transitions[state_number].append(
                    (first, last, next_state_number)
                )

        transitions[state_number].sort()

    accepts = [state.nullable() for state in states]
    error = states[NULL]

    return transitions, accepts, error
