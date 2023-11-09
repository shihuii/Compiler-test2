from Reg2Nfa import parse_regex, print_nfa

stateNum = 0
SUB_BRACE_REGEX_FLAG = '@'

regex = "(a|b)*cd"
nfa = parse_regex(regex)
if nfa:
    print("NFA created successfully!")
    print("Printing NFA:")
    print_nfa(nfa)