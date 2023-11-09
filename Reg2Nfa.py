from collections import deque

stateNum = 0
SUB_BRACE_REGEX_FLAG = '@'

class NfaNode:

    def __init__(self, isEnd=False, isEpsilon=False, stateNum=0):
        self.isEnd = isEnd
        self.isEpsilon = isEpsilon
        self.stateNum  = stateNum
        self.epsilonTransitions = []
        self.transition = {}

# 在给定一个布尔值参数 isEnd 的情况下，该函数创建一个新的NfaNode对象，并为其分配一个唯一的状态编号（通过全局变量 stateNum）。这个状态编号在NFA中用于标识不同的节点。函数返回新创建的节点对象
def create_state(isEnd):
    
    node = NfaNode()
    node.isEnd = isEnd
    node.isEpsilon = False
    global stateNum
    node.stateNum = stateNum # 先赋值
    stateNum = stateNum + 1 # 再运算
    return node


class Nfa:
    def __init__(self, startNode, endNode):
        self.startNode = startNode
        self.endNode = endNode

def create_nfa():

    start_node = create_state(False)
    end_node = create_state(True)
    return Nfa(start_node, end_node)


def parse_regex(regex):
    stackNfa = []
    stackOperator = []

    if regex:

        # TODO
        it = iter(regex)
        cur = next(it, None)

        if not cur or (not cur.isalpha() and cur != '('):
            print(f"regex:{regex} is not started with alphabet")
            return None
        
        if cur.isalpha():
            nfa = Nfa(create_state(False), create_state(True))
            nfa.startNode.transition[cur] = nfa.endNode
            stackNfa.append(nfa)

        stackOperator.append(cur)

        while cur := next(it, None):
            top = stackOperator[-1] if stackOperator else None

            if cur.isalpha():
                if top and (top.isalpha() or top == SUB_BRACE_REGEX_FLAG or top == '*'):
                    nfa = stackNfa[-1]
                    end_node = create_state(True)
                    nfa.endNode.transition[cur] = end_node
                    nfa.endNode.isEnd = False
                    nfa.endNode = end_node

                    stackOperator.pop()
                    stackOperator.append(cur)
                    continue
            
                if top == '|':
                    curnfa = create_nfa()
                    curnfa.startNode.transition[cur] = curnfa.endNode

                    newNfa = create_nfa()
                    topnfa = stackNfa[-1]

                    newNfa.startNode.isEpsilon = True
                    newNfa.startNode.epsilonTransitions.extend([curnfa.startNode, topnfa.startNode])

                    curnfa.endNode.isEpsilon = True
                    topnfa.endNode.isEpsilon = True
                    topnfa.endNode.isEnd = False
                    curnfa.endNode.isEnd = False
                    curnfa.endNode.epsilonTransitions.extend([newNfa.endNode])
                    topnfa.endNode.epsilonTransitions.extend([newNfa.endNode])

                    stackNfa.pop() # pop操作
                    stackNfa.append(newNfa)
                    stackOperator.pop()
                    stackOperator.append(cur)
                    continue
            
                if top == '(':

                    # curnfa = Nfa(create_state(False), create_state(True))
                    curnfa = create_nfa()
                    curnfa.startNode.transition[cur] = curnfa.endNode
                    stackNfa.append(curnfa)
                    stackOperator.append(cur)
                    continue
            
            if cur == '(':
                stackOperator.append(cur)
                continue

            if cur == '|':
                if top in ['(', '|']:
                    print("illegal brace or | operator")
                    break

                stackOperator.pop()
                stackOperator.append(cur)
                continue

            if cur == ')':
                if top in ['|', '(']:
                    print("illegal brace or | operator")
                    break

                stackOperator.pop()

                if not stackOperator:
                    print("miss match brace")
                    break
                
                top = stackOperator[-1] #原本是pop,改为top
                 
                if top != '(':
                    print("miss match brace")
                    break

                stackOperator.pop() # 现在才pop

                if stackOperator:
                    top = stackOperator[-1]

                    if top.isalpha():
                        if len(stackNfa) < 2:
                            print("miss match left regex")
                            break

                        # TODO
                        first = stackNfa.pop()
                        second = stackNfa.pop()

                        second.startNode.transition.clear()
                        second.startNode.transition[top] = first.startNode
                        del second.endNode
                        second.endNode = first.endNode
                        stackNfa.append(second)
                        stackOperator.pop()
                    
                    if top == '|':
                        if len(stackNfa) < 2:
                            print("miss match left regex")
                            break

                        first = stackNfa.pop()
                        second = stackNfa.pop()

                        newNfa = create_nfa()
                        newNfa.startNode.isEpsilon = True
                        newNfa.startNode.epsilonTransitions.extend([first.startNode, second.startNode])

                        first.endNode.isEnd = False
                        second.endNode.isEnd = False
                        first.endNode.isEpsilon = True
                        second.endNode.isEpsilon = True
                        first.endNode.epsilonTransitions.extend([newNfa.endNode])
                        second.endNode.epsilonTransitions.extend([newNfa.endNode])

                        stackNfa.append(newNfa)
                        stackOperator.pop()

                    if top == '*':
                        if len(stackNfa) < 2:
                            print("miss match regex")
                            break

                        first = stackNfa.pop()
                        second = stackNfa.pop()

                        second.endNode.isEnd = False
                        second.endNode.isEpsilon = first.startNode.isEpsilon
                        second.endNode.transition = first.startNode.transition
                        second.endNode.epsilonTransitions = first.startNode.epsilonTransitions

                        del first.startNode
                        stackNfa.append(second)
                        stackOperator.pop()

                # TODO
                stackOperator.append(SUB_BRACE_REGEX_FLAG)
                continue

            if cur == '*':
                if top == '*':
                    continue

                if top in ['|', '(']:
                    print("ileagal regex")
                    break

                if not stackNfa:
                    print("empty NFA stack , invalid regex")
                    break

                nfa = create_nfa()
                top = stackNfa[-1]

                nfa.startNode.isEpsilon = True
                nfa.startNode.epsilonTransitions.extend([top.startNode, nfa.endNode])

                top.endNode.isEnd = False
                top.endNode.isEpsilon = True
                top.endNode.epsilonTransitions.extend([nfa.endNode, top.startNode])

                # TODO
                stackNfa.pop()
                stackNfa.append(nfa)
                stackOperator.pop()
                stackOperator.append(cur)       

    print(f"NFA stack size:{len(stackNfa)}")
    return stackNfa[0] if len(stackNfa) == 1 else None

def print_nfa(nfa):
    if not nfa:
        return

    visited_nodes = set()
    visited = deque([nfa.startNode])

    while visited:
        node = visited.popleft()

        if node in visited_nodes:
            continue

        if node.isEpsilon:
            for epsilon_node in node.epsilonTransitions:
                print(f"{node.stateNum}---Epsilon---{epsilon_node.stateNum}")
                visited.append(epsilon_node)

        for symbol, transition_node in node.transition.items():
            print(f"{node.stateNum}---{symbol}---{transition_node.stateNum}")
            visited.append(transition_node)

        visited_nodes.add(node)

        # 检查终止节点是否正确
        # if node.isEnd:
        #     print(f"EndNode: {'true' if node == nfa.endNode else 'false'} stateNum: {node.stateNum}")


# # 测试
# # Test
# regex = "(a|b)*cd"
# nfa = parse_regex(regex)
# if nfa:
#     print("NFA created successfully!")
#     print("Printing NFA:")
#     print_nfa(nfa)
