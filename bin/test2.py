import os
import sys
import basic

if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    path = os.path.join(os.path.dirname(__file__), '..' , 'dnd1.basic')
interpreter = basic.Interpreter(path)
interpreter.run()
