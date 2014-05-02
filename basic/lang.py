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

    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return "Restore({0.expression!r})".format(self)

    def __str__(self):
        return "RESTORE #{0.expression}".format(self)


class Reference():

    def __init__(self, variable, indices):
        self.variable = variable
        self.indices = indices

    def __repr__(self):
        return "Reference({0.variable}, {0.indices!r})".format(self)

    def __str__(self):
        if len(self.indices):
            indices_str = ",".join(map(str, self.indices))
            return "{0}({1})".format(self.variable, indices_str)
        else:
            return self.variable
