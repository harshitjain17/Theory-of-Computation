class DFA:
    def __init__(self, alphabet, states, start_state, accept_states, transitions):
        """
        Initializes a Deterministic Finite Automaton (DFA) instance.

        Args:
        - alphabet: Set of characters in the alphabet.
        - states: Set of states in the DFA.
        - start_state: Start state of the DFA.
        - accept_states: Set of accept states in the DFA.
        - transitions: List of transition tuples (source state, destination state, label).
        """

        self.alphabet = set(alphabet)
        self.states = set(states)
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.transitions = {state: {} for state in states}
        for (src, dest, label) in transitions:
            self.transitions[src][label] = dest

    def accepts(self, string):
        """
        Determines whether the DFA accepts the given input string.

        Args:
        - string: Input string to be checked for acceptance.

        Returns:
        - True if the DFA accepts the input string, False otherwise.
        """

        current_state = self.start_state
        for character in string:
            if character in self.transitions[current_state]:
                current_state = self.transitions[current_state][character]
            else:
                return False
        return current_state in self.accept_states

class NFA:
    def __init__(self, alphabet, states, start_state, accept_states, transitions):
        """
        Initializes a Non-deterministic Finite Automaton (NFA) instance.

        Args:
        - alphabet: Set of characters in the alphabet.
        - states: Set of states in the NFA.
        - start_state: Start state of the NFA.
        - accept_states: Set of accept states in the NFA.
        - transitions: List of transition tuples (source state, destination state, label).
        """

        self.alphabet = set(alphabet)
        self.states = set(states)
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.transitions = {state: {} for state in states}
        for (src, dest, label) in transitions:
            if label in self.transitions[src]:
                self.transitions[src][label].add(dest)
            else:
                self.transitions[src][label] = {dest}

    def epsilon_closure(self, states):
        """
        Computes the epsilon closure of a set of states in the NFA.

        Args:
        - states: Set of states for which epsilon closure needs to be computed.

        Returns:
        - Set of states reachable from the input states via epsilon transitions.
        """

        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if 'EPSILON' in self.transitions[state]:
                for next_state in self.transitions[state]['EPSILON']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def move(self, states, label):
        """
        Computes the set of states reachable from a set of states via a given label.

        Args:
        - states: Set of states from which transitions are to be explored.
        - label: Label representing the transition.

        Returns:
        - Set of states reachable from the input states via the given label.
        """

        new_states = set()
        for state in states:
            if label in self.transitions[state]:
                new_states = new_states.union(self.transitions[state][label])
        return new_states

    def accepts(self, string):
        """
        Determines whether the NFA accepts the given input string.

        Args:
        - string: Input string to be checked for acceptance.

        Returns:
        - True if the NFA accepts the input string, False otherwise.
        """

        current_states = self.epsilon_closure([self.start_state])
        for character in string:
            current_states = self.epsilon_closure(self.move(current_states, character))
        return not current_states.isdisjoint(self.accept_states)

def read_automaton(file_path):
    """
    Reads the description of an automaton from a file and returns its parameters.

    Args:
    - file_path: Path to the file containing the automaton description.

    Returns:
    - Tuple containing the alphabet, states, start state, accept states, and transitions of the automaton.
    """

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    alphabet = lines[0]

    states_count = int(lines[1])
    states = lines[2:2 + states_count]

    start_state = lines[2 + states_count]

    accept_states_count = int(lines[3 + states_count])
    accept_states = lines[4 + states_count:4 + states_count + accept_states_count]

    transitions_count = int(lines[4 + states_count + accept_states_count])
    transitions = [
        tuple(line.split(',')) for line in lines[5 + states_count + accept_states_count:]
    ]

    return alphabet, states, start_state, accept_states, transitions

def main():

    # Main function to test the DFA and NFA    
    dfa_file = 'dfalarge.txt'
    nfa_file = 'nfalarge.txt'

    # Read automaton descriptions from files
    dfa_alphabet, dfa_states, dfa_start_state, dfa_accept_states, dfa_transitions = read_automaton(dfa_file)
    nfa_alphabet, nfa_states, nfa_start_state, nfa_accept_states, nfa_transitions = read_automaton(nfa_file)

    # Create DFA and NFA instances
    dfa = DFA(dfa_alphabet, dfa_states, dfa_start_state, dfa_accept_states, dfa_transitions)
    nfa = NFA(nfa_alphabet, nfa_states, nfa_start_state, nfa_accept_states, nfa_transitions)

    # Prompt user for input string to check
    string_to_check = input("Enter the string to check: ")

    # Check if the DFA and NFA accept the input string
    print(f"DFA accepts string: {dfa.accepts(string_to_check)}")
    print(f"NFA accepts string: {nfa.accepts(string_to_check)}")

if __name__ == "__main__":
    main()