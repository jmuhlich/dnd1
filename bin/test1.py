import basic.parser
import os

p = basic.parser.Parser()
path = os.path.join(os.path.dirname(__file__), '..' , 'dnd1.basic')
with open(path) as f:
    grammar = p.grammar(f.read())
    program = grammar.program()
for line in program.lines:
    print line
