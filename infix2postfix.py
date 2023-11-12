def priority_level(a):
    # 返回运算符的优先级，优先级定义：闭包（*）>连接符（.）>或运算（|）>括号
    if a == '(' or a == ')':
        return 1
    elif a == '|':
        return 2
    elif a == '.':
        return 3
    elif a == '*':
        return 4
    else:
        return 5


def is_operand(a):
    # 判断是否操作数，这里把数字和字母当做操作数
    if '0' <= a <= '9':
        return True
    if 'a' <= a <= 'z':
        return True
    if 'A' <= a <= 'Z':
        return True
    return False


def infix_to_postfix(infix_expression):
    # 把中缀转化为后缀，并且补上在中缀中省略的连接符
    temp = []
    j = 0
    st = []
    for i in range(len(infix_expression)):
        if is_operand(infix_expression[i]):
            temp.append(infix_expression[i])
        else:
            if not st:
                st.append(infix_expression[i])
            else:
                a = st[-1]
                if priority_level(infix_expression[i]) <= priority_level(a):
                    while priority_level(a) >= priority_level(infix_expression[i]):
                        if a != '(' and a != ')':
                            temp.append(a)
                        st.pop()
                        if not st:
                            break
                        else:
                            a = st[-1]
                    st.append(infix_expression[i])
                else:
                    st.append(infix_expression[i])
        if i < len(infix_expression) - 1:  # 判断下一个符号是不是连接符
            if (is_operand(infix_expression[i]) and infix_expression[i + 1] == '(') or \
                    (is_operand(infix_expression[i]) and is_operand(infix_expression[i + 1])) or \
                    (infix_expression[i] == '*' and is_operand(infix_expression[i + 1])) or \
                    (infix_expression[i] == '*' and infix_expression[i + 1] == '(') or \
                    (infix_expression[i] == ')' and infix_expression[i + 1] == '('):
                if not st:
                    st.append('.')
                else:
                    a = st[-1]
                    if priority_level('.') <= priority_level(a):
                        while priority_level(a) >= priority_level('.'):
                            if a != '(' and a != ')':
                                temp.append(a)
                            st.pop()
                            if not st:
                                break
                            else:
                                a = st[-1]
                        st.append('.')
                    else:
                        st.append('.')

    while st:
        if st[-1] != '(' and st[-1] != ')':
            temp.append(st[-1])
        st.pop()

    return ''.join(temp)


# if __name__ == "__main__":
#     infix_expression = input("请输入中缀表达式: ")  # 输入中缀表达式
#     postfix_expression = infix_to_postfix(infix_expression)
#     print('\n', postfix_expression, '\n')
