from tokenizer import tokenizer
from collections import deque
import math


class node(object):
    """
    Node definition for use in a parse tree.
    """

    def __init__(self, value=None, parent=None, right=None, left=None):
        self.value = value
        self.parent = parent
        self.right = right
        self.left = left


def printPostorder(root):
    if root:
        printPostorder(root.left)
        printPostorder(root.right)
        print(root.value)


def rpn(token_list):
    """Convert the provided expression to Reverse Polish Notation so it can be handled more easily.

    Parameters
    ----------
    expression : str
        A mathamatical expression in the form of a string

    Returns
    -------
    deque
        The RPN as a queue for use in the `reverse_polish` method
    """
    output = deque()
    operator = deque()
    ops = {'+': 2, '-': 2, '*': 3, '/': 3, '**': 4}

    for token in token_list:
        if token.type == 'Literal' or token.type == 'Variable':
            output.appendleft(token)
        elif token.type == 'Function':
            operator.append(token)
        elif token.type == 'Operator':
            while len(operator) > 0 and (
                    operator[-1].type == 'Function' or operator[-1].type == 'Operator' and (
                    ops[operator[-1].value] > ops[token.value] or (
                        ops[operator[-1].value] > ops[token.value] and token.value == '^')
                    )) and token.type != 'Left Parenthesis':
                output.appendleft(operator.pop())
            operator.append(token)
        elif token.value == 'Left Parenthesis':
            operator.append(token)
        elif token.value == 'Right Parenthesis':
            while operator[-1].type != 'Left Parenthesis':
                output.appendleft(operator.pop())
            if operator[-1].type == 'Left Parenthesis':
                operator.pop()
            if operator[-1].type == 'Function':
                output.appendleft(operator.pop())
    while len(operator) > 0:
        output.appendleft(operator.pop())

    return output


def build(token_list: list):
    postorder = rpn(token_list)
    if len(postorder) == 1:
        return node(value=postorder.pop())
    root = node()
    curr = root
    while len(postorder) > 0:
        token = postorder.popleft()
        if token.type == 'Operator':
            curr.value = token
            if curr.left is None:
                curr.left = node(value=None, parent=curr)
                curr = curr.left
            elif curr.right is None:
                curr.right = node(value=None, parent=curr)
                curr = curr.right
            else:
                raise ValueError(
                    f'Something weird happened when parsing {token}')
        elif token.type == 'Literal' or token.type == 'Variable':
            curr.value = token
            curr = curr.parent
            while curr.right is not None or curr.value.type == 'Function':
                if curr.parent is None:
                    return curr
                curr = curr.parent
            curr.right = node(value=None, parent=curr)
            curr = curr.right
        elif token.type == 'Function':
            curr.value = token
            curr.left = node(value=None, parent=curr)
            curr = curr.left
        else:
            raise ValueError(f'Something weird happened when parsing {token}')
    return None


def solve_side(root: node):
    if root.value.type == 'Literal':
        return root.value.value
    if root.value.type == 'Function':
        temp = eval(f'math.{root.value.value}({solve_side(root.left)})')
        return temp
    if root.value.type == 'Operator':
        temp = eval(
            f'{solve_side(root.right)} {root.value.value} {solve_side(root.left)}')
        return temp
    raise ValueError(f'Oops {root.value}')


def solve(equation):

    expression = tokenizer(equation)
    left_side = right_side = None
    comp = None
    for i, token in enumerate(expression):
        if token.type == 'Comparator':
            left_side = build(expression[:i])
            right_side = build(expression[i+1:])
            comp = token.value
            break
    if comp is None:
        expression = build(expression)
        print(f'The answer is {solve_side(expression)}')
    else:
        if comp == '=':
            comp = '=='
        result = eval(
            f'{solve_side(left_side)} {comp} {solve_side(right_side)}')
        print(f'The equation is {result}')
