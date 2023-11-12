from infix2postfix import infix_to_postfix
from postfix2nfa import str_to_nfa,print_nfa

infix_expression = input("请输入中缀表达式: ")
postfix_expression = infix_to_postfix(infix_expression)
nfa_instance = str_to_nfa(postfix_expression)
nodes,edges = print_nfa(nfa_instance)