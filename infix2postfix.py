OperatorPriority = {
    '*': 4,
    '?': 4,
    '+': 4,
    '.': 3,
    '|': 2,
    '(': 1
}

def infix_to_postfix(str):
    output = []
    ops = []
    is_last_ch = False

    def pushOperator(op):
        priority = OperatorPriority[op]
        while ops:
            top = ops.pop()
            if OperatorPriority[top] >= priority:
                output.append(top)
            else:
                ops.append(top)
                break
        ops.append(op)

    for i in range(len(str)):
        ch = str[i]

        if ch in ('*', '?', '+'):
            pushOperator(ch)
            is_last_ch = True
            continue

        if ch == '|':
            pushOperator(ch)
            is_last_ch = False
            continue

        if ch == '(':
            if is_last_ch:
                pushOperator('.')
            ops.append(ch)
            is_last_ch = False
            continue

        if ch == ')':
            op = ops.pop()
            while op:
                if op == '(':
                    break
                output.append(op)
                op = ops.pop()

            if op != '(':
                raise ValueError(f'no "(" match ")" at [{i}] of "{str}"')

            is_last_ch = True
            continue

        # normal char
        if is_last_ch:
            pushOperator('.')
        output.append(ch)
        is_last_ch = True

    

    while ops:
        op = ops.pop()
        if op == '(':
            raise ValueError(f'not matched "(" of "{str}"')
        output.append(op)

    return ''.join(output)

# result = regex2post("(a*|b*|c*)* ")
# print(result)
