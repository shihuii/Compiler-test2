def nodes_to_with(nodes,edges):
    cnt = 0
    while cnt != len(nodes):
        cnt = len(nodes)
        for i in edges:
            if i[0] in nodes and i[-1] == 'ε' and i[1] not in nodes:
                nodes.append(i[1])
    return nodes


def nfa_to_dfa(nfa_nodes,nfa_edges):
    dfa_nodes = []
    dfa_edges = []

    #找到0通过ε可以到达的所有点
    nodes0 = nodes_to_with([0],nfa_edges)

    temp = [nodes0] #中间变量，用于作为队列
    temp_nodes = [nodes0] #中间变量，储存变化过程中出现过的点
    temp_edges = [] #中间变量，储存变化过程中出现过的边
    edges_without_ = [] #不含ε的边
    chars = [] #所有字符
    for i in nfa_edges:
        if i[-1] != 'ε':
            if i[-1] not in chars:
                chars.append(i[-1])
            edges_without_.append(i)

    while temp != []:
        
        now = temp.pop()
        to = []

        for i in chars:
            
            for j in edges_without_:
                if j[0] in now and j[-1] == i:
                    to.append(j[1])

            to = nodes_to_with(to,nfa_edges)

            if to != [] and to not in temp_nodes:
                temp_nodes.append(to)
                temp.append(to)
                temp_edges.append([now,to,i])
                to = []

    cnt = len(temp_nodes)

    for i in range(0,cnt):
        book = 0
        for j in temp_nodes[i]:
            if nfa_nodes[j][2] == 'end':
                book = 1
                break

        if book == 1:
            dfa_nodes.append((i,str(i),'end'))
        else:
            dfa_nodes.append((i,str(i),''))

    for i in temp_edges:
        dfa_edges.append((temp_nodes.index(i[0]),temp_nodes.index(i[1]),i[2]))

    return dfa_nodes , dfa_edges

if __name__ == '__main__':
    # 定义节点列表
    nodes = [(0, '0', 'end'), (1, '1', ''), (2, '2', ''), (3, '3', ''),
    (4, '4', ''),(5, '5', ''), (6, '6', ''), (7, '7', ''),
    (8, '8', ''), (9, '9', ''), (10, '10', ''), (11, '11', ''), 
    (12, '12', 'end')]
    # 定义边列表
    edges = [(0, 1, 'a'), (1, 5, 'ε'), (2, 3, 'b'), (3, 5, 'ε'),
            (4, 2, 'ε'), (4, 0, 'ε'), (5, 4, 'ε'), (5, 7, 'ε'),
            (6, 4, 'ε'), (6, 7, 'ε'), (7, 8, 'ε'), (8, 9, 'a'),
            (9, 10, 'ε'), (10, 11, 'b'), (11, 12, 'ε')]
    nodes,edges = nfa_to_dfa(nodes,edges)
    print(nodes)
    print(edges)