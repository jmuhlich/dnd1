class Program(object):

    def __init__(self, lines):
        self.lines = lines

    def __repr__(self):
        return "Program(<{0} lines>)".format(len(self.lines))


class Line(object):

    def __init__(self, number, statement):
        self.number = number
        self.statement = statement

    def __repr__(self):
        return "Line({0.number}, {0.statement!r})".format(self)

    def __str__(self):
        return "{0.number} {0.statement}".format(self)


class Statement(object):
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
        return "LET {0.reference} = {0.expression}".format(self)


class Print(Statement):

    def __init__(self, args=None):
        self.args = []
        if args is not None:
            for a in args:
                if isinstance(a, list):
                    self.args.extend(a)
                elif a is not None:
                    self.args.append(a)

    def __repr__(self):
        if self.args:
            return "Print({0.args!r})".format(self)
        else:
            return "Print()"

    def __str__(self):
        if self.args:
            args_str = ''.join(str(a) for a in self.args)
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


class Todo(Statement):

    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return "Todo({0.string!r})".format(self)

    def __str__(self):
        return "<<TODO>> {0.string}".format(self)


class Reference(object):

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


class Negation(object):

    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return "Negation({0.expression!r})".format(self)

    def __str__(self):
        return "-{0.expression}".format(self)


class Parens(object):

    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return "Parens({0.expression!r})".format(self)

    def __str__(self):
        return "({0.expression})".format(self)


class Mul(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "Mul({0.a!r}, {0.b!r})".format(self)

    def __str__(self):
        return "{0.a}*{0.b}".format(self)


class Div(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "Div({0.a!r}, {0.b!r})".format(self)

    def __str__(self):
        return "{0.a}/{0.b}".format(self)


class Add(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "Add({0.a!r}, {0.b!r})".format(self)

    def __str__(self):
        return "{0.a}+{0.b}".format(self)


class Sub(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "Sub({0.a!r}, {0.b!r})".format(self)

    def __str__(self):
        return "{0.a}-{0.b}".format(self)


# Consider this class abstract; only instantiate its subclasses.
class Builtin(object):

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


class StringLiteral(object):

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return "String({0.content!r})".format(self)

    def __str__(self):
        return '"{0.content}"'.format(self)


class FileSpec(object):

    def __init__(self, handle, name):
        self.handle = handle
        self.name = name

    def __repr__(self):
        return "FileSpec({0.handle!r}, {0.name!r})".format(self)

    def __str__(self):
        return "#{0.handle}={0.name}".format(self)
