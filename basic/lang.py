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

    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return "Restore({0.num!r})".format(self)

    def __str__(self):
        return "RESTORE #{0.num}".format(self)


class Let(Statement):

    def __init__(self, reference, expression):
        self.reference = reference
        self.expression = expression

    def __repr__(self):
        return "Let({0.reference!r}, {0.expression!r})".format(self)

    def __str__(self):
        return "LET {0.reference} = {0.expression}".format(self)


class Print(Statement):

    def __init__(self, arg1=None, argn=None, lsep=None):
        self.args = []
        if arg1 is not None:
            self.args.append(arg1)
        if argn is not None:
            self.args += sum(argn, [])
        if lsep is not None:
            self.args.append(lsep)

    def __repr__(self):
        return "Print({0.args!r})".format(self)

    def __str__(self):
        if self.args:
            args_str = ''.join(str(a) for a in self.args)
            return "PRINT {0}".format(args_str)
        else:
            return "PRINT"


class Todo(Statement):

    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return "Todo({0.string!r})".format(self)

    def __str__(self):
        return "<<TODO>> {0.string}".format(self)


class Reference(object):

    def __init__(self, variable, indices):
        self.variable = variable
        self.indices = indices

    def __repr__(self):
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
