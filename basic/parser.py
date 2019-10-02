from . import lang
import parsley # type: ignore

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

str_value = string | str_ref

expr = (expr:left ws '+' ws expr2:right -> basic.Add(left, right)) \
     | (expr:left ws '-' ws expr2:right -> basic.Sub(left, right)) \
     | expr2
expr2 = (expr2:left ws '*' ws value:right -> basic.Mul(left, right)) \
      | (expr2:left ws '/' ws value:right -> basic.Div(left, right)) \
      | value

bool = (bool:left sp 'AND' sp bool:right -> basic.And(left, right)) \
     | (bool:left sp 'OR' sp bool:right -> basic.Or(left, right)) \
     | bool2
bool2 = (str_value:left sp '=' sp str_value:right \
        -> basic.StringEqual(left, right)) \
      | (str_value:left sp '<>' sp str_value:right \
        -> basic.StringNotEqual(left, right)) \
      | (expr:left sp '=' sp expr:right -> basic.Equal(left, right)) \
      | (expr:left sp '<>' sp expr:right -> basic.NotEqual(left, right)) \
      | (expr:left sp '<=' sp expr:right -> basic.LessOrEqual(left, right)) \
      | (expr:left sp '<' sp expr:right -> basic.Less(left, right)) \
      | (expr:left sp '>=' sp expr:right -> basic.GreaterOrEqual(left, right)) \
      | (expr:left sp '>' sp expr:right -> basic.Greater(left, right))

index_2 = '(' expr:expr1 ',' expr:expr2 ')' -> [expr1, expr2]
index_1 = '(' expr:expr ')' -> [expr]
indices = index_2 | index_1
num_ref_scalar = numvar:var -> basic.Reference(var)
num_ref_array = numvar:var indices:indices -> basic.Reference(var, indices)
num_ref = num_ref_array | num_ref_scalar
str_ref = strvar:var indices?:indices -> basic.Reference(var, indices)
any_ref = str_ref | num_ref
dim_2 = '(' integer:d1 ',' integer:d2 ')' -> [d1, d2]
dim_1 = '(' integer:d1 ')' -> [d1]
dim_ref = (strvar|numvar):var (dim_2|dim_1):dims -> basic.Reference(var, dims)
fh_literal = '#' integer
fh_ref = ('#' num_ref) | fh_literal

builtin_arg = '(' expr:expr ')' -> expr
int = 'INT' builtin_arg:expr -> basic.Int(expr)
abs = 'ABS' builtin_arg:expr -> basic.Abs(expr)
rnd = 'RND' builtin_arg:expr -> basic.Rnd(expr)
clk = 'CLK' builtin_arg:expr -> basic.Clk(expr)

print_arg1 = (str_value | expr):arg -> arg
print_argn_zone = ',' sp print_arg1:arg -> arg
print_argn_immediate = ';' sp print_arg1:arg -> arg

filespec = fh_literal:handle '=' string:name -> basic.FileSpec(handle, name)

comment = 'REM' (' ' sp <char*> | -> ''):content -> basic.Comment(content)
base = 'BASE ' sp integer:num -> basic.Base(num)
restore = 'RESTORE ' sp fh_ref:fh -> basic.Restore(fh)
let = ('LET ' sp)? num_ref:ref sp '=' sp expr:expr -> basic.Let(ref, expr)
# Not sure why using '*' on the first two alternatives didn't work, and instead
# I had to use '+' and split the single-arg cases out on their own.
print = ('PRINT ' sp print_arg1:arg1 sp print_argn_zone+:argn sp ','?:lsep \
         -> basic.Print([arg1] + argn, basic.Print.ZONE, lsep is None)) \
      | ('PRINT ' sp print_arg1:arg1 sp print_argn_immediate+:argn sp ';'?:lsep \
         -> basic.Print([arg1] + argn, basic.Print.IMMEDIATE, lsep is None)) \
      | ('PRINT ' sp print_arg1:arg1 sp ',' \
         -> basic.Print([arg1], basic.Print.ZONE, False)) \
      | ('PRINT ' sp print_arg1:arg1 sp ';' \
         -> basic.Print([arg1], basic.Print.IMMEDIATE, False)) \
      | ('PRINT ' sp print_arg1:arg1 \
         -> basic.Print([arg1], basic.Print.ZONE, True)) \
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
for = 'FOR ' sp num_ref_scalar:ref sp '=' expr:start sp 'TO' sp expr:end \
      -> basic.For(ref, start, end)
next = 'NEXT ' sp num_ref_scalar:ref -> basic.Next(ref)
if = 'IF ' sp bool:expr sp ('THEN' | 'GO' ' '? 'TO') sp integer:line_number \
     -> basic.If(expr, line_number)
goto = 'GO' ' '? 'TO ' sp integer:line_number -> basic.Goto(line_number)
gosub = 'GOSUB ' sp integer:line_number -> basic.Gosub(line_number)
return = 'RETURN' -> basic.Return()
stop = 'STOP' -> basic.Stop()
end = 'END' -> basic.End()

statement = comment | base | restore | let | print | dim | read | write \
          | file | data | input | for | next | if | goto | gosub | return \
          | stop | end

line = sp integer:num ' ' sp statement:stmt sp nl -> basic.Line(num, stmt)

program = line*:lines -> basic.Program(lines)

"""

class Parser:

    def __init__(self):
        self.grammar = parsley.makeGrammar(
            grammar_source, {'basic': lang}
        )

    def parse(self, text) -> lang.Program:
        parsley_parser = self.grammar(text)
        return parsley_parser.program()
