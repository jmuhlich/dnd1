class Program:

    def __init__(self, lines):
        self.lines = lines

    def __repr__(self):
        return "Program(<{0} lines>)".format(len(self.lines))


class Line:

    def __init__(self, number, statement):
        self.number = number
        self.statement = statement

    def __repr__(self):
        return "Line({0.number}, {0.statement!r})".format(self)

    def __str__(self):
        return "{0.number} {0.statement}".format(self)


class Statement:
    pass


class Comment(Statement):

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return "Comment('{0.content}')".format(self)

    def __str__(self):
        if len(self.content):
            return "REM {0.content}".format(self)
        else:
            return "REM"


class Base(Statement):

    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "Base({0.number})".format(self)

    def __str__(self):
        return "BASE {0.number}".format(self)


class Restore(Statement):

    def __init__(self, fh):
        self.fh = fh

    def __repr__(self):
        return "Restore({0.fh!r})".format(self)

    def __str__(self):
        return "RESTORE #{0.fh}".format(self)


class Let(Statement):

    def __init__(self, reference, expression):
        self.reference = reference
        self.expression = expression

    def __repr__(self):
        return "Let({0.reference!r}, {0.expression!r})".format(self)

    def __str__(self):
        return "LET {0.reference}={0.expression}".format(self)


class Print(Statement):

    ZONE = 1
    IMMEDIATE = 2

    def __init__(self, args=None, control=None, newline=True):
        if args is not None:
            self.args = args
        else:
            self.args = []
        self.control = control
        self.newline = newline

    def __repr__(self):
        if self.args:
            if self.control == Print.ZONE:
                control = 'ZONE'
            else:
                control = 'IMMEDIATE'
            return ("Print({0.args!r}, {1}, {0.newline!r})" \
                    .format(self, control))
        else:
            return "Print()"

    def __str__(self):
        if self.args:
            separator = ',' if self.control == Print.ZONE else ';'
            args_str = separator.join(str(a) for a in self.args)
            if not self.newline:
                args_str += separator
            return "PRINT {0}".format(args_str)
        else:
            return "PRINT"


class Dim(Statement):

    def __init__(self, var_refs):
        self.var_refs = var_refs

    def __repr__(self):
        return "Dim({0.var_refs!r})".format(self)

    def __str__(self):
        refs_str = ",".join(str(r) for r in self.var_refs)
        return "DIM {0}".format(refs_str)


class Read(Statement):

    def __init__(self, fh, var_refs):
        self.fh = fh
        self.var_refs = var_refs

    def __repr__(self):
        return "Read({0.fh!r}, {0.var_refs!r})".format(self)

    def __str__(self):
        args_str = ",".join(str(r) for r in self.var_refs)
        if self.fh is not None:
            args_str = '#{0},'.format(self.fh) + args_str
        return "READ {0}".format(args_str)


class Write(Statement):

    def __init__(self, fh, var_refs):
        self.fh = fh
        self.var_refs = var_refs

    def __repr__(self):
        return "Write({0.fh!r}, {0.var_refs!r})".format(self)

    def __str__(self):
        args_str = ",".join(str(r) for r in self.var_refs)
        if self.fh is not None:
            args_str = '#{0},'.format(self.fh) + args_str
        return "WRITE {0}".format(args_str)


class File(Statement):

    def __init__(self, filespecs):
        self.filespecs = filespecs

    def __repr__(self):
        return "File({0.filespecs!r})".format(self)

    def __str__(self):
        filespecs_str = ",".join(str(s) for s in self.filespecs)
        return "FILE {0}".format(filespecs_str)


class Data(Statement):

    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return "Data({0.values!r})".format(self)

    def __str__(self):
        values_str = ",".join(str(v) for v in self.values)
        return "DATA {0}".format(values_str)


class Input(Statement):

    def __init__(self, var_refs):
        self.var_refs = var_refs

    def __repr__(self):
        return "Input({0.var_refs!r})".format(self)

    def __str__(self):
        vars_str = ",".join(str(r) for r in self.var_refs)
        return "INPUT {0}".format(vars_str)


class For(Statement):

    def __init__(self, var_ref, start, end):
        self.var_ref = var_ref
        self.start = start
        self.end = end

    def __repr__(self):
        return "For({0.var_ref!r}, {0.start!r}, {0.end!r})".format(self)

    def __str__(self):
        return "FOR {0.var_ref}={0.start} TO {0.end}".format(self)


class Next(Statement):

    def __init__(self, var_ref=None):
        self.var_ref = var_ref

    def __repr__(self):
        if self.var_ref is None:
            return "Next()"
        else:
            return "Next({0.var_ref!r})".format(self)

    def __str__(self):
        if self.var_ref is None:
            return "NEXT"
        else:
            return "NEXT {0.var_ref}".format(self)


class If(Statement):

    def __init__(self, expr, line_number):
        self.expr = expr
        self.line_number = line_number

    def __repr__(self):
        return "If({0.expr!r}, {0.line_number!r})".format(self)

    def __str__(self):
        return "IF {0.expr} THEN {0.line_number}".format(self)


class Goto(Statement):

    def __init__(self, line_number):
        self.line_number = line_number

    def __repr__(self):
        return "Goto({0.line_number!r})".format(self)

    def __str__(self):
        return "GO TO {0.line_number}".format(self)


class Gosub(Statement):

    def __init__(self, line_number):
        self.line_number = line_number

    def __repr__(self):
        return "Gosub({0.line_number!r})".format(self)

    def __str__(self):
        return "GOSUB {0.line_number}".format(self)


class Return(Statement):

    def __repr__(self):
        return "Return()"

    def __str__(self):
        return "RETURN"


class Stop(Statement):

    def __repr__(self):
        return "Stop()"

    def __str__(self):
        return "STOP"


class End(Statement):

    def __repr__(self):
        return "End()"

    def __str__(self):
        return "END"


class Reference:

    def __init__(self, variable, indices=None):
        self.variable = variable
        self.indices = indices

    def __repr__(self):
        if self.indices is None:
            return "Reference('{0.variable}')".format(self)
        else:
            return "Reference('{0.variable}', {0.indices!r})".format(self)

    def __str__(self):
        if self.indices is None:
            return self.variable
        else:
            indices_str = ",".join(map(str, self.indices))
            return "{0}({1})".format(self.variable, indices_str)


class Negation:

    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return "Negation({0.expression!r})".format(self)

    def __str__(self):
        return "-{0.expression}".format(self)


class Parens:

    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return "Parens({0.expression!r})".format(self)

    def __str__(self):
        return "({0.expression})".format(self)


class Mul:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "Mul({0.a!r}, {0.b!r})".format(self)

    def __str__(self):
        return "{0.a}*{0.b}".format(self)


class Div:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "Div({0.a!r}, {0.b!r})".format(self)

    def __str__(self):
        return "{0.a}/{0.b}".format(self)


class Add:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "Add({0.a!r}, {0.b!r})".format(self)

    def __str__(self):
        return "{0.a}+{0.b}".format(self)


class Sub:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "Sub({0.a!r}, {0.b!r})".format(self)

    def __str__(self):
        return "{0.a}-{0.b}".format(self)


# Consider this class abstract; only instantiate its subclasses.
class BooleanOperator:

    symbol = '<undefined>'

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "{1}({0.a!r}, {0.b!r})".format(self, type(self).__name__)

    def __str__(self):
        return "{0.a} {1} {0.b}".format(self, self.symbol)


class And(BooleanOperator):
    symbol = 'AND'

class Or(BooleanOperator):
    symbol = 'OR'


# Consider this class abstract; only instantiate its subclasses.
class Comparison:

    symbol = '<undefined>'

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "{1}({0.a!r}, {0.b!r})".format(self, type(self).__name__)

    def __str__(self):
        return "{0.a}{1}{0.b}".format(self, self.symbol)


class StringEqual(Comparison):
    symbol = '='

class StringNotEqual(Comparison):
    symbol = '<>'

class Equal(Comparison):
    symbol = '='

class NotEqual(Comparison):
    symbol = '<>'

class LessOrEqual(Comparison):
    symbol = '<='

class Less(Comparison):
    symbol = '<'

class GreaterOrEqual(Comparison):
    symbol = '>='

class Greater(Comparison):
    symbol = '>'


# Consider this class abstract; only instantiate its subclasses.
class Builtin:

    lang_name = '<undefined>'

    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return "{1}({0.expression!r})".format(self, type(self).__name__)

    def __str__(self):
        return "{1}({0.expression})".format(self, self.lang_name)


class Int(Builtin):
    lang_name = 'INT'


class Abs(Builtin):
    lang_name = 'ABS'


class Rnd(Builtin):
    lang_name = 'RND'


class Clk(Builtin):
    lang_name = 'CLK'


class StringLiteral:

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return "String({0.content!r})".format(self)

    def __str__(self):
        return '"{0.content}"'.format(self)


class FileSpec:

    def __init__(self, handle, name):
        self.handle = handle
        self.name = name

    def __repr__(self):
        return "FileSpec({0.handle!r}, {0.name!r})".format(self)

    def __str__(self):
        return "#{0.handle}={0.name}".format(self)
