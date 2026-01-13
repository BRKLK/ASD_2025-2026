def check_brackets(expr: str) -> bool:
    counter = 0
    for el in expr:
        if el == '(': counter += 1
        elif el == ')': counter -= 1
        if counter < 0: return False
    if counter != 0:
        return False
    return True

def perform_op(a, b, op):
    if op == "+":
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b != 0:
            return a / b
        else:
            raise ZeroDivisionError


priors = {"+": 1, "-": 1, "*": 2, "/": 2}

def MyEval(expr: str) -> float:
    expr = expr.replace(' ', '')
    # expr = expr[:-1] # removing the "=" sign 
    if not check_brackets(expr):
        print("Wrong brackets placement")
        return

    # Dividing elements
    nums = []
    ops = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        
        # getting numbers
        if ch.isdigit():
            start = i
            while (i < len(expr)) and (expr[i].isdigit() or expr[i] == '.'):
                i += 1
            end = i
            nums.append(float(expr[start : end]))

        # getting operators
        if ch in "+-*/":
            ops.append(ch)
            i += 1
        
        # counting expresions in brackets
        if ch == '(':
            j = len(expr) - 1
            while i < j:
                if expr[j] == ")":
                    nums.append(MyEval(expr[i+1 : j]))
                    break
                j -= 1
            i = j + 1

    # performing Multiplications and divisions
    nums_new = [nums[0]]
    ops_new = []
    for i, op in enumerate(ops):
        if priors[op] == 1:
            nums_new.append(nums[i+1])
            ops_new.append(op)
        elif priors[op] == 2:
            nums_new[-1] = perform_op(nums_new[-1], nums[i+1], op)

    # performing additions and subtractions
    value = nums_new[0]
    for i, op in enumerate(ops_new):
        value = perform_op(value, nums_new[i+1], op)
    
    return value

text = input("input: ")
res = MyEval(text)
print(res)
    
