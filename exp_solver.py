from collections import deque


class parser(object):
    """
    Holds the methods for parsing an expression.
    I know this could've been done with an eval(). That wasn't the point.
    """
    @staticmethod
    def parse(expression: str):
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
        ops = {'+': 2, '-': 2, '*': 3, '/': 3, '^': 4}

        for token in expression:
            if token in '0123456789':
                output.appendleft(token)
            # elif token in function:
            #     operator.append(token)
            elif token in '+-*/^':
                while len(operator) > 0 and operator[-1] in '+-*/^' and (
                        ops[operator[-1]] > ops[token] or (
                            ops[operator[-1]] > ops[token] and token == '^')
                ) and token != '(':
                    output.appendleft(operator.pop())
                operator.append(token)
            elif token == '(':
                operator.append(token)
            elif token == ')':
                while operator[-1] != '(':
                    output.appendleft(operator.pop())
                if operator[-1] == '(':
                    operator.pop()
                # if operator[-1] in function:
                #     output.appendleft(operator.pop())
        while len(operator) > 0:
            output.appendleft(operator.pop())

        return output

    @staticmethod
    def reverse_polish(expression: deque) -> float:
        """Computes the value of expresions provided in RPN

        Parameters
        ----------
        expression : deque
            Expression in RPN, typically from `parse` 

        Returns
        -------
        float
            The floating point value of the expression
        """
        evaluation = []

        while len(expression) > 0:
            token = expression.pop()
            if token in '0123456789':
                evaluation.append(token)
            elif token in '+-*/^':
                if token == '^':
                    token = '**'
                operands = [evaluation.pop(), evaluation.pop()]
                evaluation.append(eval(f'{operands[1]} {token} {operands[0]}'))

        return evaluation[0]


expression = '4*(3-2)+3^(7-3)'
print(parser.reverse_polish(parser.parse(expression)))
