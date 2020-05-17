from string import digits, ascii_letters
from collections import deque
import re

VARIABLES = dict()

def clear_expression(expr):
    expr = expr.split()
    expr = ''.join(expr)
    expr = re.sub('\+-+', '-', expr)
    expr = re.sub('-\++', '-', expr)
    expr = re.sub('--', '+', expr)
    expr = re.sub('\++', '+', expr)
    expr = re.sub('\+-+', '-', expr)
    expr = re.sub('-\++', '-', expr)
    expr = re.sub('^\+', '0+', expr)
    expr = re.sub('^-', '0-', expr)
    expr = re.sub('\(\+', '(0+', expr)
    expr = re.sub('\(-', '(0-', expr)
    number_or_symbol = re.compile('(\d+|[^ 0-9])')
    expr = re.findall(number_or_symbol, expr)
    return expr

def check_brackets(s):
    stack = deque()
    for c in s:
        if c == '(':
            stack.append(c)
        elif c == ')':
            if not stack or stack.pop() != '(':
                return False
    if stack:
        return False
    return True


def infix_to_postfix(s):
    global VARIABLES
    operators = ('+', '-', '/', '*', '^')
    brackets = ('(', ')')
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = deque()
    postfix_expr = []
    for c in s:
        if c not in operators and c not in brackets:
            postfix_expr.append(c)
        elif c in operators and (not stack or stack[-1] == '('):
            stack.append(c)
        elif c in operators and precedence[c] > precedence[stack[-1]]:
            stack.append(c)
        elif c in operators and precedence[c] <= precedence[stack[-1]]:
            while stack and stack[-1] != '(' and precedence[c] <= precedence[stack[-1]]:
                postfix_expr.append(stack.pop())
            stack.append(c)
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                postfix_expr.append(stack.pop())
            stack.pop()
    while stack:
        postfix_expr.append(stack.pop())
    return postfix_expr

def calculate_postfix(postfix_expr):
    stack = deque()
    try:
        for c in postfix_expr:
            if c.isalpha():
                stack.append(VARIABLES[c])
            elif c.isdigit():
                stack.append(c)
            elif c == '+':
                stack.append(str(float(stack.pop()) + float(stack.pop())))
            elif c == '-':
                second = float(stack.pop())
                first = float(stack.pop())
                stack.append(str(first - second))
            elif c == '*':
                stack.append(str(float(stack.pop()) * float(stack.pop())))
            elif c == '/':
                second = float(stack.pop())
                first = float(stack.pop())
                stack.append(str(first / second))
            elif c == '^':
                second = float(stack.pop())
                first = float(stack.pop())
                stack.append(str(first ** second))
        print(stack.pop().rstrip('0').rstrip('.'))
        return True
    except KeyError:
        print('Unknown variable')
        return True
    except Exception:
        print('Invalid expression')
        return True

def help():
    print('The program calculates the sum of numbers')

def process_commands(command):
    if command == '/help':
        help()
    elif command == '/exit':
        print('Bye!')
        return False
    print('Unknown command')
    return True

def is_command(q):
    if q[0] == '/':
        return True
    else:
        return False

def process_expressions(expr):
    clear_expr = clear_expression(expr)
    if not check_brackets(clear_expr):
        print('Invalid expression')
        return True
    postfix_expr = infix_to_postfix(clear_expr)
    calculate_postfix(postfix_expr)
    return True

def is_expression(exp):
    acceptable_symbols = {'+', '-', ' ', '(', ')', '*', '/', '^', ''}
    acceptable_symbols = acceptable_symbols.union(set(digits))
    acceptable_symbols = acceptable_symbols.union(set(ascii_letters))
    for c in ''.join(exp.split()):
        if c not in acceptable_symbols:
            print('Invalid expression')
            return False
    return True

def is_valid_identifier(var):
    return var.isalpha()

def is_assignment(var_expr):
    if '=' in var_expr:
        return True
    return False

def assignment(var_expr):
    global VARIABLES
    var, expr = var_expr.split('=', maxsplit=1)
    var = var.strip(' ')
    expr = expr.strip(' ')
    if not is_valid_identifier(var):
        print('Invalid identifier')
        return True
    if expr.isalpha():
        if expr not in VARIABLES:
            print('Unknown variable')
            return True
        VARIABLES[var] = VARIABLES[expr]
        return True
    try:
        VARIABLES[var] = expr
        return True
    except:
        print('Invalid assignment')
        return True


def process_query(q):
    if not q:
        return True
    elif is_command(q):
        return process_commands(q)
    elif is_assignment(q):
        return assignment(q)
    elif is_expression(q):
        return process_expressions(q)
    return True


while True:
    query = input()
    res = process_query(query)
    if not res:
        break



