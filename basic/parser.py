import basic
import parsley

grammar_source = """
spaces = ' '+
char = :x ?(x != '\\n') -> x
nl = '\n'
number = <digit+>:ds -> int(ds)

comment = 'REM' (spaces <char*> | -> ''):content -> basic.Comment(content)
other = <char+>

statement = comment | other

line = spaces? number:num spaces statement:stmt spaces? nl -> \
  basic.Line(num, stmt)

"""

class Parser(object):

    def __init__(self):
        self.grammar = parsley.makeGrammar(grammar_source, {'basic': basic})
