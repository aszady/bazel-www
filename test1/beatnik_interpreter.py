import sys
import os.path
from scrabble import punkty

# specyfikacja niejasna, płytki do scrabbli utknęły w odpływie umywalki
# ten "interpreter" pod spodem tak naprawdę "kompiluje" cały kod przed wykonaniem
# Nie obsługiwałem innych błędów niż "file not found"

# system importów jest zaimplementowany za pomocą słowa kluczowego "import2137"
# następne słowo jest nazwą importowanego pliku

stack = []
ip = 0; # instruction "pointer"
prog = [] # instructions and their arguments
def noop():
    global ip; ip += 1;
def push():
    global ip; ip += 2;
    stack.append(prog[ip-1])
def pop():
    global ip; ip += 1;
    return stack.pop()
def add():
    global ip; ip += 1;
    stack.append(stack.pop()+stack.pop())
def getch(): # input character, and push its ASCII value
    global ip; ip += 1;
    stack.append(ord(input()[0])) # excessive chars are discarded
def printch(): # pop value, and print it as ASCII character
    global ip; ip += 1;
    print(chr(stack.pop()), end='')
def substract(): # pop two numbers, from second one substract first, and push result
    global ip; ip += 1;
    first = stack.pop()
    second = stack.pop()
    stack.append(first - second)
def swap(): # pop two numbers, swap them, and push them back
    global ip; ip += 1;
    a = stack.pop(); b = stack.pop()
    stack.append(b); stack.append(a)
def dup(): # pop a number and push it twice
    global ip; ip += 1;
    a = stack.pop(); stack.append(a); stack.append(a)
def ahead_on_zero():
    global ip; ip += 2;
    if(stack[-1] == 0): ip += prog[ip]
def ahead_on_not_zero():
    global ip; ip += 2;
    if(stack[-1] != 0): ip += prog[ip]
def back_on_zero():
    global ip; ip += 2;
    if(stack[-1] != 0): ip -= prog[ip-1]
def back_on_not_zero():
    global ip; ip += 2;
    if(stack[-1] != 0): ip -= prog[ip-1]
def exit_():
    exit()

def parse(filename):
    if not os.path.isfile(filename):
        print("file %s not found" % filename)
        exit(1)

    tok_lookup = {
     5:push, 6:pop, 7:add, 8:getch, 9:printch, 10:substract, 11:swap, 12:dup,
     13:ahead_on_zero, 14:ahead_on_not_zero, 15:back_on_zero,16:back_on_not_zero,
     17:exit_}
    tokens_with_args = [push,ahead_on_zero,ahead_on_not_zero,back_on_zero,back_on_not_zero]

    arg = False; # True if next parsed token is argument to previous instruction (other than import)
    importArg = False; # True if next parsed token is argument to import
    tokens = []
    with open(filename) as file:
        for line in file:
            for word in line.split():
                if importArg: 
                    tokens += parse(word)
                    importArg = False;
                elif word == "import2137":
                    importArg = True;
                else:
                    points = punkty(word);
                    token = points if arg else tok_lookup.get(points, noop)
                    arg = True if (token in tokens_with_args) else False
                    tokens.append(token)
    return tokens;

# print tokens in pretty form. Handy for debugging
def pretty_tok(tok):
    if(callable(tok)): return f"{tok.__name__}"
    else: return tok;
def pretty_print_tokens(tokens):
    print('# tokens = [', end='')
    for tok in tokens[:-1]:
        print(pretty_tok(tok), end=", ")
    if(len(tokens) > 0): print(pretty_tok(tokens[-1]), end="]\n")
    else: print("]")

if __name__ == '__main__':
    prog = parse(sys.argv[1])
    if(prog[-1] != exit_): prog.append(exit_);
    pretty_print_tokens(prog)
    while(True):
        prog[ip]()
