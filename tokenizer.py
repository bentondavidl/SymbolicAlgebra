import re


class token(object):
    """
    Representation for Literals, Variables, Operators, and Functions
    """

    def __init__(self, _type, value):
        """
        Constructor for token class
        """
        self.type = _type
        self.value = value

    def __repr__(self):
        return f'{self.type}:{self.value}'

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value


def tokenizer(equation: str) -> list:
    """
    Converts equation strings to a list of tokens.
    """
    equation = re.sub(r'([+\-*\/=<>])-([\d.]*)', r'\1 (0-\2)', equation)
    out = []
    number_buffer = []
    letter_buffer = []
    for char in equation:
        if re.match(r'\d|\.', char):
            number_buffer.append(char)
        elif re.match(r'[a-zA-Z]', char):
            if len(number_buffer) > 0:
                out.append(token('Literal', ''.join(number_buffer)))
                number_buffer = []
            letter_buffer.append(char)
        elif re.match(r'[+\-\/*\^]', char):
            if len(number_buffer) > 0:
                out.append(token('Literal', ''.join(number_buffer)))
                number_buffer = []
            elif len(letter_buffer) > 0:
                for letter in letter_buffer:
                    out.append(token('Variable', letter))
                letter_buffer = []
            if char == '^':
                char = '**'
            out.append(token('Operator', char))
        elif char == '(':
            if len(letter_buffer) > 0:
                out.append(token('Function', ''.join(letter_buffer)))
                letter_buffer = []
            elif len(number_buffer) > 0:
                out.append(token('Literal', ''.join(number_buffer)))
                number_buffer = []
                out.append(token('Operator', '*'))
            out.append(token('Left Parenthesis', char))
        elif char == ')':
            if len(number_buffer) > 0:
                out.append(token('Literal', ''.join(number_buffer)))
                number_buffer = []
            elif len(letter_buffer) > 0:
                for letter in letter_buffer:
                    out.append(token('Variable', letter))
                letter_buffer = []
            out.append(token('Right Parenthesis', char))
        elif char == ',':
            if len(number_buffer) > 0:
                out.append(token('Literal', ''.join(number_buffer)))
                number_buffer = []
            elif len(letter_buffer) > 0:
                for letter in letter_buffer:
                    out.append(token('Variable', letter))
                letter_buffer = []
            out.append(token('Function Argument Separator', char))
        elif re.match(r'[=<>]', char):
            if len(number_buffer) > 0:
                out.append(token('Literal', ''.join(number_buffer)))
                number_buffer = []
            elif len(letter_buffer) > 0:
                for letter in letter_buffer:
                    out.append(token('Variable', letter))
                letter_buffer = []
            out.append(token('Comparator', char))

    if len(number_buffer) > 0:
        out.append(token('Literal', ''.join(number_buffer)))
        number_buffer = []
    if len(letter_buffer) > 0:
        for letter in letter_buffer:
            out.append(token('Variable', letter))
        letter_buffer = []
    return out


# print(tokenizer('-444 +3.6 xa-  v(-3,5)'))
