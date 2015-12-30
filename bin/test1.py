from basic import Parser
import os

parser = Parser()
path = os.path.join(os.path.dirname(__file__), '..' , 'dnd1.basic')
with open(path) as f:
    program = parser.parse(f.read())
for line in program.lines:
    print line
