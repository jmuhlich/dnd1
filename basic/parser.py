import basic
import parsley

grammar_source = """
sp = ' '*
char = :x ?(x != '\\n') -> x
nl = '\n'
integer = <digit+>:ds -> int(ds)
number = (( <digit+ '.' digit*> | <digit* '.' digit+> ):ds -> float(ds)) | integer
varname = <letter letterOrDigit*>
numvar = varname
strvar = <varname '$'>
string = '"' <(:c ?(c != '"'))+>:content '"' -> basic.StringLiteral(content)
literal = number | string

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
any_ref = str_ref | num_ref
dim_2 = '(' integer:d1 ',' integer:d2 ')' -> (d1, d2)
dim_1 = '(' integer:d1 ')' -> (d1,)
dim_ref = (strvar|numvar):var (dim_2|dim_1):dims -> basic.Reference(var, dims)
fh_literal = '#' integer
fh_ref = ('#' num_ref) | fh_literal

builtin_arg = '(' expr:expr ')' -> expr
int = 'INT' builtin_arg:expr -> basic.Int(expr)
abs = 'ABS' builtin_arg:expr -> basic.Abs(expr)
rnd = 'RND' builtin_arg:expr -> basic.Rnd(expr)
clk = 'CLK' builtin_arg:expr -> basic.Clk(expr)

print_sep = <';'|','>
print_arg1 = (str_ref | string | expr):arg -> arg
print_argn = print_sep:sep sp print_arg1:arg -> [sep, arg]

filespec = fh_literal:handle '=' string:name -> basic.FileSpec(handle, name)

comment = 'REM' (' ' sp <char*> | -> ''):content -> basic.Comment(content)
base = 'BASE ' sp integer:num -> basic.Base(num)
restore = 'RESTORE ' sp fh_ref:fh -> basic.Restore(fh)
let = ('LET ' sp)? num_ref:ref sp '=' sp expr:expr -> basic.Let(ref, expr)
print = ('PRINT ' sp print_arg1:arg1 sp print_argn*:argn sp print_sep?:lsep \
         -> basic.Print([arg1] + argn + [lsep])) \
      | ('PRINT' -> basic.Print())
dim = 'DIM ' sp dim_ref:ref1 (sp ',' sp dim_ref)*:refn -> basic.Dim([ref1] + refn)
read = 'READ ' (sp fh_ref:fh sp ',' -> fh)?:fh sp any_ref:ref1 \
       (sp ',' sp any_ref)*:refn -> basic.Read(fh, [ref1] + refn)
write = 'WRITE ' (sp fh_ref:fh sp ',' -> fh)?:fh sp any_ref:ref1 \
        (sp ',' sp any_ref)*:refn -> basic.Write(fh, [ref1] + refn)
file = 'FILE ' sp filespec:fs1 (sp ',' sp filespec)*:fsn \
       -> basic.File([fs1] + fsn)
data = 'DATA ' sp literal:val1 sp (sp ',' sp literal)*:valn \
       -> basic.Data([val1] + valn)
input = 'INPUT ' sp any_ref:ref1 (sp ',' sp any_ref)*:refn \
        -> basic.Input([ref1] + refn)
goto = 'GO' ' '? 'TO ' sp integer:line_number -> basic.Goto(line_number)
gosub = 'GOSUB ' sp integer:line_number -> basic.Gosub(line_number)
return = 'RETURN' -> basic.Return()
stop = 'STOP' -> basic.Stop()
end = 'END' -> basic.End()


# FIXME this is a fall-through for testing - delete it when finished
todo = <char+>:todo_stmt -> basic.Todo(todo_stmt)

statement = comment | base | restore | let | print | dim | read | write \
          | file | data | input | goto | gosub | return | stop | end | todo

line = sp integer:num ' ' sp statement:stmt sp nl -> basic.Line(num, stmt)

program = line*:lines -> basic.Program(lines)

"""

class Parser(object):

    def __init__(self):
        self.grammar = parsley.makeGrammar(grammar_source,
                                           {'basic': basic.lang})
