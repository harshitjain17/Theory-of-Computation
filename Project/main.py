class DFA:
    def __init__(self, alphabet, states, start_state, accept_states, transitions):
        self.alphabet = set(alphabet)
        self.states = set(states)
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.transitions = {state: {} for state in states}
        for (src, dest, label) in transitions:
            self.transitions[src][label] = dest

    def accepts(self, string):
        current_state = self.start_state
        for character in string:
            if character in self.transitions[current_state]:
                current_state = self.transitions[current_state][character]
            else:
                return False
        return current_state in self.accept_states

class NFA:
    def __init__(self, alphabet, states, start_state, accept_states, transitions):
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
        new_states = set()
        for state in states:
            if label in self.transitions[state]:
                new_states = new_states.union(self.transitions[state][label])
        return new_states

    def accepts(self, string):
        current_states = self.epsilon_closure([self.start_state])
        for character in string:
            current_states = self.epsilon_closure(self.move(current_states, character))
        return not current_states.isdisjoint(self.accept_states)

def read_automaton(file_path):
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
    dfa_file = 'dfadesc.txt'
    nfa_file = 'nfadesc.txt'

    dfa_alphabet, dfa_states, dfa_start_state, dfa_accept_states, dfa_transitions = read_automaton(dfa_file)
    nfa_alphabet, nfa_states, nfa_start_state, nfa_accept_states, nfa_transitions = read_automaton(nfa_file)

    dfa = DFA(dfa_alphabet, dfa_states, dfa_start_state, dfa_accept_states, dfa_transitions)
    nfa = NFA(nfa_alphabet, nfa_states, nfa_start_state, nfa_accept_states, nfa_transitions)

    string_to_check = input("Enter the string to check: ")
    print(f"DFA accepts string: {dfa.accepts(string_to_check)}")
    print(f"NFA accepts string: {nfa.accepts(string_to_check)}")

if __name__ == "__main__":
    main()