import sys
import os
import random
import operator
from basic import Parser, lang


class Interpreter(object):

    def __init__(self, source_path, trace=None):
        self.source_path = source_path
        if trace is None:
            trace = len(os.getenv('BASIC_TRACE', '')) > 0
        self.trace = trace

        self.parser = Parser()
        self.scalar_symbols = {}
        self.array_symbols = {}
        self.line_index = 0
        self.data_line_index = 0
        self.data_item_index = 0
        self.loop_stack = []
        self.sub_stack = []
        self.files = {}

        self.parse_source()

    def parse_source(self):
        with open(self.source_path) as f:
            self.program = self.parser.parse(f.read())

    def run(self):
        try:
            while self.line_index < len(self.program.lines):
                self.step()
        except ProgramStop:
            pass
        print "\n< Program terminated >"

    def step(self):
        line = self.program.lines[self.line_index]
        self.exec_line(line)

    def current_line_number(self):
        return self.program.lines[self.line_index].number

    def exec_line(self, line):
        if self.trace:
            print >> sys.stderr, '>>> {}'.format(line)
        statement = line.statement
        statement_name = type(statement).__name__
        handler_name = 'stmt_' + statement_name
        try:
            handler = getattr(self, handler_name)
        except AttributeError:
            msg = "Interpreter does not implement '{0}'".format(statement_name)
            raise BasicNotImplementedError(msg)
        flow_changed = handler(statement)
        if not flow_changed:
            self.line_index += 1

    def jump_to_line(self, line_number):
        line_iter = (i for i, l in enumerate(self.program.lines)
                     if l.number == line_number)
        try:
            line_index = next(line_iter)
        except StopIteration:
            msg = "Line {} does not exist in this program".format(line_number)
            raise BasicRuntimeError(msg)
        self.line_index = line_index

    def stmt_Base(self, st):
        if st.number != 0:
            raise BasicNotImplementedError(
                'Only "Base 0" is currently implemented')
        return False

    def stmt_Comment(self, st):
        return False

    def stmt_Data(self, st):
        # This has no direct effect, rather we will scan for Data statements
        # upon execution of Read statements.
        return False

    def stmt_Dim(self, st):
        for ref in st.var_refs:
            name = ref.variable
            dims = [i + 1 for i in ref.indices]
            array_class = StringArray if name.endswith('$') else NumericArray
            if len(dims) == 1:
                dims.append(1)
            array = array_class(dims)
            self.array_symbols[name] = array
        return False

    def stmt_End(self, st):
        raise ProgramStop

    def stmt_File(self, st):
        for fs in st.filespecs:
            if fs.handle in self.files:
                msg = "File #{0} already opened".format(fs.handle)
                raise BasicRuntimeError(msg)
            name = fs.name.content
            f = open(name, 'rw')
            self.files[fs.handle] = f
        return False

    def stmt_For(self, st):
        if (not self.loop_stack or
            self.loop_stack[-1].for_index != self.line_index):
            frame = LoopFrame(st.var_ref, self.eval_expr(st.start),
                              self.eval_expr(st.end), self.line_index,
                              self.find_next_index())
            self.loop_stack.append(frame)
            self.write_reference(frame.var_ref, frame.start)
        else:
            frame = self.loop_stack[-1]
        counter = self.read_reference(frame.var_ref)
        if counter > frame.end:
            self.line_index = frame.next_index + 1
            self.loop_stack.pop()
            return True
        else:
            return False

    def find_next_index(self):
        for_var = self.program.lines[self.line_index].statement.var_ref.variable
        depth = 0
        for i, line in enumerate(self.program.lines[self.line_index+1:],
                                 self.line_index+1):
            if isinstance(line.statement, lang.For):
                depth += 1
            if isinstance(line.statement, lang.Next):
                if depth > 0:
                    depth -= 1
                    continue
                next_var = line.statement.var_ref.variable
                if next_var is not None and next_var != for_var:
                    msg = ("NEXT statement on line {} has mismatched variable"
                           .format(line.number))
                    raise BasicRuntimeError(msg)
                else:
                    return i
        msg = ("FOR statement on line {} has no matching NEXT"
               .format(self.current_line_number()))
        raise BasicRuntimeError(msg)

    def stmt_If(self, st):
        result = self.eval_expr(st.expr)
        if result:
            self.jump_to_line(st.line_number)
            return True
        else:
            return False

    def stmt_Input(self, st):
        num_vars = len(st.var_refs)
        is_numeric = [not n.variable.endswith('$') for n in st.var_refs]
        values = []
        while True:
            try:
                content = raw_input('?')
            except EOFError:
                raise ProgramStop
            values = content.split(',')
            if len(values) < num_vars:
                print >> sys.stderr, "Too few values"
            elif len(values) > num_vars:
                print >> sys.stderr, "Too few values"
            else:
                break
        for i, v in enumerate(values):
            if is_numeric[i]:
                try:
                    v = float(v)
                except ValueError:
                    # Return 0 when we can't parse input as a number.
                    v = 0.0
                values[i] = v
        for ref, value in zip(st.var_refs, values):
            self.write_reference(ref, value)
        return False

    def stmt_Let(self, st):
        value = self.eval_expr(st.expression)
        self.write_reference(st.reference, value)
        return False

    def stmt_Next(self, st):
        frame = self.loop_stack[-1]
        counter = self.read_reference(frame.var_ref)
        self.write_reference(frame.var_ref, counter + 1)
        self.line_index = frame.for_index
        return True

    def stmt_Print(self, st):
        for arg in st.args:
            value = self.eval_expr(arg)
            if st.control == st.ZONE:
                sys.stdout.write('%-14s' % value)
            else:
                # FIXME implement proper numeric formatting (esp. spaces)
                sys.stdout.write('%s' % value)
        if st.newline:
            sys.stdout.write('\n')
        return False

    def stmt_Restore(self, st):
        handle = self.eval_expr(st.fh)
        if handle not in self.files:
            raise BasicRuntimeError("File #{0} not open".format(handle))
        self.files[handle].seek(0)
        return False

    def stmt_Stop(self, st):
        raise ProgramStop

    def eval_expr(self, expr):
        term_name = type(expr).__name__
        handler_name = 'term_' + term_name
        try:
            handler = getattr(self, handler_name)
        except AttributeError:
            msg = "Interpreter does not implement '{0}'".format(term_name)
            raise BasicNotImplementedError(msg)
        return handler(expr)

    def term_int(self, expr):
        return float(expr)

    def term_float(self, expr):
        return expr

    def term_StringLiteral(self, expr):
        return expr.content

    def term_Reference(self, expr):
        return self.read_reference(expr)

    def math_op(self, expr, op):
        a = self.eval_expr(expr.a)
        b = self.eval_expr(expr.b)
        return op(a, b)

    def term_Add(self, expr):
        return self.math_op(expr, operator.add)

    def term_Sub(self, expr):
        return self.math_op(expr, operator.sub)

    def term_Mul(self, expr):
        return self.math_op(expr, operator.mul)

    def term_Div(self, expr):
        return self.math_op(expr, operator.div)

    def string_op(self, expr, op):
        a = self.eval_expr(expr.a).lower()
        b = self.eval_expr(expr.b).lower()
        return op(a, b)

    def term_StringEqual(self, expr):
        return self.string_op(expr, operator.eq)

    def term_StringNotEqual(self, expr):
        return self.string_op(expr, operator.ne)

    # It's unclear what this is supposed to do, and it's only used in dnd1 as an
    # arg to RND (whose arg is explicitly ignored).
    def term_Clk(self, expr):
        return 0

    def term_Rnd(self, expr):
        # Produce random floats in the open interval (0, 1)
        r = 0.0
        while r == 0.0:
            r = random.random()
        return r

    def term_Int(self, expr):
        return int(self.eval_expr(expr.expression))

    def read_reference(self, reference):
        name, indices = self.resolve_reference(reference)
        if indices is None:
            value = self.scalar_symbols[name]
        else:
            value = self.array_symbols[name][indices]
        return value

    def write_reference(self, reference, value):
        name, indices = self.resolve_reference(reference)
        if indices is None:
            self.scalar_symbols[name] = value
        else:
            self.array_symbols[name][indices] = value

    def resolve_reference(self, reference):
        name = reference.variable
        if reference.indices is None:
            indices = None
        else:
            indices = [self.eval_expr(i) for i in reference.indices]
        return name, indices


class Array(object):

    def __init__(self, dims):
        self.dim1, self.dim2 = dims
        self.data = [self.FILL] * (self.dim1 * self.dim2)

    def __getitem__(self, indices):
        i1, i2 = indices
        return self.data[i1 * self.dim2 + i2]

    def __setitem__(self, indices, value):
        i1, i2 = indices
        self.data[i1 * self.dim2 + i2] = value


class NumericArray(Array):
    FILL = 0


class StringArray(Array):
    FILL = ''


class LoopFrame(object):

    def __init__(self, var_ref, start, end, for_index, next_index):
        self.var_ref = var_ref
        self.start = start
        self.end = end
        self.for_index = for_index
        self.next_index = next_index


class ProgramStop(Exception):
    "Signal that the program has executed the STOP statement."


class BasicNotImplementedError(Exception):
    "Feature of the BASIC language hasn't been implemented yet."


class BasicRuntimeError(Exception):
    "Runtime error in the BASIC interpreter."


if __name__ == '__main__':
    path = sys.argv[1]
    interpreter = Interpreter(path)
