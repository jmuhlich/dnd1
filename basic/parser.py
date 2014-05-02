import basic
import parsley

grammar_source = """
sp = ' '*
spr = ' '+  # r=required
char = :x ?(x != '\\n') -> x
nl = '\n'
number = <digit+>:ds -> int(ds)
varname = <letter letterOrDigit*>
numvar = varname
strvar = <varname> '$'
string = '"' <(:c ?(c != '"'))+> '"'

basic_num_expr = number | numvar
# FIXME - implement
# num_expr = ...
reference = varname:var (num_expr (',' num_expr)*)?:indices -> \
  basic.Reference(var, indices)

comment = 'REM' (spr <char*> | -> ''):content -> basic.Comment(content)
base = 'BASE' spr number:num -> basic.Base(num)
restore = 'RESTORE' spr '#' num_expr:expr -> basic.Restore(expr)
let = ('LET' spr)? reference:ref sp '=' sp

# FIXME this is a fall-through for testing - delete it when finished
other = <char+>

statement = comment | base | restore | other

line = sp number:num spr statement:stmt sp nl -> basic.Line(num, stmt)

"""

class Parser(object):

    def __init__(self):
        self.grammar = parsley.makeGrammar(grammar_source,
                                           {'basic': basic.lang})
