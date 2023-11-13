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
            # TODO
            nfa_instance.delta.setdefault(pre, {}).setdefault(postfix_expression[i], []).append(nxt)
        elif postfix_expression[i] == '*':
            pre = st_end.pop()
            nxt = st_begin.pop()
            nfa_instance.delta.setdefault(pre, {}).setdefault('ε', []).append(nxt)
            nfa_instance.Q.add(status_id)
            # pre1 = status_id  改 先赋值，再加一
            pre1 = status_id
            status_id += 1
            nfa_instance.Q.add(status_id)
            # status_id += 1
            # nxt1 = status_id 改 先赋值，再加一
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

            # TODO 原代码中没有这一句
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

def generate_nfa(nfa_instance):

    print('graph LR')
    nodes = set()
    edges = []

    for state in nfa_instance.Q:
        for symbol in nfa_instance.sigma:
            # 相比于原代吗，可以更安全地处理不存在的键
            if symbol in nfa_instance.delta.get(state, {}):
                for nxt_state in nfa_instance.delta[state][symbol]:
                    if nfa_instance.q0 == state:
                        nodes.add((state, f"{state}", 'begin'))
                        nodes.add((nxt_state, f"{nxt_state}", ''))
                        edges.append((state, nxt_state, symbol))
                    # TODO 和原代码不一样
                    elif nxt_state in nfa_instance.F:
                        nodes.add((state, f"{state}", ''))
                        nodes.add((nxt_state, f"{nxt_state}", 'end'))
                        edges.append((state, nxt_state, symbol))
                    else:
                        nodes.add((state, f"{state}", ''))
                        nodes.add((nxt_state, f"{nxt_state}", ''))
                        edges.append((state, nxt_state, symbol))

    formatted_nodes = list(nodes)

    # TODO 原代吗中没有
    formatted_nodes.sort(key=lambda x: x[0])  # 按状态号排序

    formatted_nodes_list = list(formatted_nodes)

    for i, node in enumerate(formatted_nodes_list):
        if node[2] == 'begin':
            begin_state = node[0]
            begin_name = node[1]
            
            # 创建一个新的元组，并替换原列表中的元组
            formatted_nodes_list[i] = (begin_state, begin_name, '')

    # 将修改后的列表转换回元组
    formatted_nodes = tuple(formatted_nodes_list)

    print(enumerate(edges))

    for i, edge in enumerate(edges):
        if edge[0] == 0 or edge[0] == begin_state:
            edges[i] = (begin_state if edge[0] == 0 else 0, edge[1], edge[2])
        if edge[1] == 0 or edge[1] == begin_state:
            edges[i] = (edge[0], begin_state if edge[1] == 0 else 0, edge[2])


    print("Nodes:", formatted_nodes)
    print("Edges:", edges)

    return formatted_nodes, edges
    

# if __name__ == "__main__":
#     postfix_expression = 'ab|*a.b.b.'
#     nfa_instance = str_to_nfa(postfix_expression)
#     generate_nfa(nfa_instance)
