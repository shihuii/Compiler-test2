class NFA:
    def __init__(self):
        self.Q = set()                     # 状态集合
        self.sigma = set()                 # 输入字符集合
        self.delta = {}                    # 状态转移函数
        self.q0 = None                     # 初始状态
        self.F = set()                     # 接收状态集合


def is_operand(a):
    return a.isdigit() or a.isalpha()


def str_to_nfa(postfix_expression):
    status_id = 0
    st_begin = []
    st_end = []
    nfa_instance = NFA()

    for i in range(len(postfix_expression)):
        if is_operand(postfix_expression[i]):
            nfa_instance.sigma.add(postfix_expression[i])
            pre = status_id
            nfa_instance.Q.add(status_id)
            st_begin.append(status_id)
            status_id += 1
            nxt = status_id
            nfa_instance.Q.add(status_id)
            st_end.append(status_id)
            status_id += 1
            nfa_instance.delta.setdefault(pre, {}).setdefault(postfix_expression[i], []).append(nxt)
        elif postfix_expression[i] == '*':
            pre = st_end.pop()
            nxt = st_begin.pop()
            nfa_instance.delta.setdefault(pre, {}).setdefault('ε', []).append(nxt)
            nfa_instance.Q.add(status_id)
            pre1 = status_id
            nfa_instance.Q.add(status_id)
            status_id += 1
            nxt1 = status_id
            status_id += 1
            nfa_instance.delta.setdefault(pre1, {}).setdefault('ε', []).append(nxt)
            nfa_instance.delta.setdefault(pre, {}).setdefault('ε', []).append(nxt1)
            nfa_instance.delta.setdefault(pre1, {}).setdefault('ε', []).append(nxt1)
            st_begin.append(pre1)
            st_end.append(nxt1)
        elif postfix_expression[i] == '.':
            pre1 = st_begin.pop()
            pre2 = st_begin.pop()
            nxt1 = st_end.pop()
            nxt2 = st_end.pop()
            nfa_instance.delta.setdefault(nxt2, {}).setdefault('ε', []).append(pre1)
            st_begin.append(pre2)
            st_end.append(nxt1)
        elif postfix_expression[i] == '|':
            nfa_instance.Q.add(status_id)
            pre = status_id
            status_id += 1
            nfa_instance.Q.add(status_id)
            nxt = status_id
            status_id += 1
            if not st_begin or not st_end:
                print("Error: Not enough operands for | operator")
                return nfa_instance

            pre1 = st_begin.pop()
            pre2 = st_begin.pop()
            nxt1 = st_end.pop()
            nxt2 = st_end.pop()

            nfa_instance.delta.setdefault(pre, {}).setdefault('ε', []).append(pre1)
            nfa_instance.delta.setdefault(pre, {}).setdefault('ε', []).append(pre2)
            nfa_instance.delta.setdefault(nxt1, {}).setdefault('ε', []).append(nxt)
            nfa_instance.delta.setdefault(nxt2, {}).setdefault('ε', []).append(nxt)

            st_begin.append(pre)
            st_end.append(nxt)

    nfa_instance.q0 = st_begin[-1]
    nfa_instance.F.add(st_end[-1])
    nfa_instance.sigma.add('ε')
    return nfa_instance

def print_nfa(nfa_instance):
    nodes = []
    edges = []

    for state in nfa_instance.Q:
        for symbol in nfa_instance.sigma:
            if symbol in nfa_instance.delta.get(state, {}):
                for nxt_state in nfa_instance.delta[state][symbol]:
                    if nfa_instance.q0 == state:
                        nodes.append((state,str(state),'begin'))
                        edges.append((state,nxt_state,symbol))
                    elif nxt_state in nfa_instance.F:
                        nodes.append((state,str(state),'end'))
                        edges.append((state,nxt_state,symbol))
                    else:
                        nodes.append((state,str(state),''))
                        edges.append((state,nxt_state,symbol))

    print("Nodes:", nodes)
    print("Edges:", edges)
                    
    return nodes, edges
    


# if __name__ == "__main__":
#     postfix_expression = 'ab|*a.b.b.'
#     nfa_instance = str_to_nfa(postfix_expression)
#     print_nfa(nfa_instance)
