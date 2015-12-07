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
builtin = int | abs | rnd | clk
value = number | builtin | num_ref | parens | negation

expr = (expr:left ws '+' ws expr2:right -> basic.Add(left, right)) \
     | (expr:left ws '-' ws expr2:right -> basic.Sub(left, right)) \
     | expr2
expr2 = (expr2:left ws '*' ws value:right -> basic.Mul(left, right)) \
      | (expr2:left ws '/' ws value:right -> basic.Div(left, right)) \
      | value

num_ref = numvar:var -> basic.Reference(var, [])
# FIXME implement array references
# ... (expr (',' expr)*)?:indices -> basic.Reference(var, indices)

builtin_arg = '(' expr:expr ')' -> expr
int = 'INT' builtin_arg:expr -> basic.Int(expr)
abs = 'ABS' builtin_arg:expr -> basic.Abs(expr)
rnd = 'RND' builtin_arg:expr -> basic.Rnd(expr)
clk = 'CLK' builtin_arg:expr -> basic.Clk(expr)

comment = 'REM' (' ' sp <char*> | -> ''):content -> basic.Comment(content)
base = 'BASE ' sp number:num -> basic.Base(num)
restore = 'RESTORE ' sp '#' (num_ref|number):num -> basic.Restore(num)
let = ('LET ' sp)? num_ref:ref sp '=' sp expr:expr -> basic.Let(ref, expr)

# FIXME this is a fall-through for testing - delete it when finished
other = <char+>

statement = comment | base | restore | let | other

line = sp number:num ' ' sp statement:stmt sp nl -> basic.Line(num, stmt)

program = line*:lines -> basic.Program(lines)

"""

class Parser(object):

    def __init__(self):
        self.grammar = parsley.makeGrammar(grammar_source,
                                           {'basic': basic.lang})
