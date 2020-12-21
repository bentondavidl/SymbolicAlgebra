# Running this file will actually work

from tree_builder import solve

print('This calculator currently supports most basic calculator functions including trigonometry.\nThere is also support for comparisons using =, <, or >.\nEnter your problem below and press Ctrl+C to exit')
while True:
    exp = input('> ')
    solve(exp)
