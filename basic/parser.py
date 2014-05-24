import basic
import parsley

grammar_source = """
sp = ' '*
char = :x ?(x != '\\n') -> x
nl = '\n'
number = <digit+>:ds -> int(ds)
varname = <letter letterOrDigit*>
numvar = varname
strvar = <varname> '$'
string = '"' <(:c ?(c != '"'))+> '"'

parens =  "(" expr:expr ")" -> basic.Parens(expr)
negation = '-' value:value -> basic.Negation(value)
value = number | num_ref | parens | negation

expr = (expr:left ws '+' ws expr2:right -> basic.Add(left, right)) \
     | (expr:left ws '-' ws expr2:right -> basic.Sub(left, right)) \
     | expr2
expr2 = (expr2:left ws '*' ws value:right -> basic.Mul(left, right)) \
      | (expr2:left ws '/' ws value:right -> basic.Div(left, right)) \
      | value

num_ref = numvar:var -> basic.Reference(var, [])
# FIXME implement array references
# ... (expr (',' expr)*)?:indices -> basic.Reference(var, indices)

comment = 'REM' (' ' sp <char*> | -> ''):content -> basic.Comment(content)
base = 'BASE ' sp number:num -> basic.Base(num)
restore = 'RESTORE ' sp '#' num_expr:expr -> basic.Restore(expr)
let = ('LET ' sp)? num_ref:ref sp '=' sp expr:expr -> basic.Let(ref, expr)

# FIXME this is a fall-through for testing - delete it when finished
other = <char+>

statement = comment | base | restore | let | other

line = sp number:num spr statement:stmt sp nl -> basic.Line(num, stmt)

"""

class Parser(object):

    def __init__(self):
        self.grammar = parsley.makeGrammar(grammar_source,
                                           {'basic': basic.lang})
