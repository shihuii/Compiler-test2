from infix2postfix import infix_to_postfix
from postfix2nfa import str_to_nfa,generate_nfa


infix_expression = '(a|b)*abb'
postfix_expression = infix_to_postfix(infix_expression)
nfa_instance = str_to_nfa(postfix_expression)
nodes,edges = generate_nfa(nfa_instance)