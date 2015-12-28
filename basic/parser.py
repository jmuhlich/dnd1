import basic
import parsley

grammar_source = """
sp = ' '*
char = :x ?(x != '\\n') -> x
nl = '\n'
integer = <digit+>:ds -> int(ds)
number = ( <digit+ ('.' digit*)?> | <digit* '.' digit+> ):ds -> float(ds)
varname = <letter letterOrDigit*>
numvar = varname
strvar = <varname '$'>
string = '"' <(:c ?(c != '"'))+>:content '"' -> basic.StringLiteral(content)

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

# Should really get N-d indexing working, but 2-d is enough for now.
index_2 = '(' expr:expr1 ',' expr:expr2 ')' -> (expr1, expr2)
index_1 = '(' expr:expr ')' -> (expr,)
indices = index_2 | index_1
num_ref = numvar:var indices?:indices -> basic.Reference(var, indices)
str_ref = strvar:var indices?:indices -> basic.Reference(var, indices)

builtin_arg = '(' expr:expr ')' -> expr
int = 'INT' builtin_arg:expr -> basic.Int(expr)
abs = 'ABS' builtin_arg:expr -> basic.Abs(expr)
rnd = 'RND' builtin_arg:expr -> basic.Rnd(expr)
clk = 'CLK' builtin_arg:expr -> basic.Clk(expr)

print_sep = <';'|','>
print_arg1 = (str_ref | string | expr):arg -> arg
print_argn = print_sep:sep sp print_arg1:arg -> [sep, arg]

comment = 'REM' (' ' sp <char*> | -> ''):content -> basic.Comment(content)
base = 'BASE ' sp integer:num -> basic.Base(num)
restore = 'RESTORE ' sp '#' (num_ref|integer):num -> basic.Restore(num)
let = ('LET ' sp)? num_ref:ref sp '=' sp expr:expr -> basic.Let(ref, expr)
print = ('PRINT ' sp print_arg1:arg1 sp print_argn*:argn sp print_sep?:lsep -> \
         basic.Print(arg1, argn, lsep)) \
      | ('PRINT' -> basic.Print())

# FIXME this is a fall-through for testing - delete it when finished
todo = <char+>:todo_stmt -> basic.Todo(todo_stmt)

statement = comment | base | restore | let | print | todo

line = sp integer:num ' ' sp statement:stmt sp nl -> basic.Line(num, stmt)

program = line*:lines -> basic.Program(lines)

"""

class Parser(object):

    def __init__(self):
        self.grammar = parsley.makeGrammar(grammar_source,
                                           {'basic': basic.lang})
