from . import parser


class Line(object):

    def __init__(self, number, statement):
        self.number = number
        self.statement = statement

    def __str__(self):
        return "{0.number} {0.statement}".format(self)


class Statement(object):
    pass


class Comment(Statement):

    def __init__(self, content):
        self.content = content

    def __str__(self):
        if len(self.content):
            return "REM {0.content}".format(self)
        else:
            return "REM"

