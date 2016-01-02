import os
import sys
import basic

path = os.path.join(os.path.dirname(__file__), '..' , 'dnd1.basic')
interpreter = basic.Interpreter(path)
interpreter.run()
