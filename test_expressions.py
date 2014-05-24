import operator
import random
import unittest
import parsley

ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.div,
    }
def binop(op, left, right):
    return ops[op](left, right)

x = parsley.makeGrammar("""
number = (<digit+>:ds -> int(ds)) | (<digit+ '.' digit+>:ds -> float(ds))
parens = '(' ws expr:e ws ')' -> e
value = number | parens | negate
negate = '-' value:v -> -v
ws = ' '*

binops1 = '+' | '-'
binops2 = '*' | '/'

expr = (expr:left ws binops1:op ws expr2:right -> binop(op, left, right)) | expr2
expr2 = (expr2:left ws binops2:op ws value:right -> binop(op, left, right)) | value
""", {'binop': binop})

def make_random_ws():
    return ' ' * random.randint(0, 2)

def make_random_expr():
    expr = ''
    punct = ops.keys()
    length = random.randint(1, 20)
    nesting = 0
    for i in xrange(length):
        indent = random.randint(0, 2)
        if indent == 1 and nesting >= 1:
            expr += ')'
            nesting -= 1
        if i > 0:
            expr += punct[random.randint(0, len(punct) - 1)]
            expr += make_random_ws()
        if indent == 0:
            expr += '('
            nesting += 1
        expr += str(random.randint(-999, 999))
        if i < length - 1:
            expr += make_random_ws()
    for n in xrange(nesting):
        expr += ')'
    return expr

random.seed(0)
failures = 0
for i in xrange(1000):
    expr = make_random_expr();
    try:
        ours = x(expr).expr()
        python = eval(expr)
    except ZeroDivisionError:
        continue
    if ours == python:
        print 'OK: {expr}'.format(**locals())
    else:
        print 'FAIL: {expr} <{ours} (ours) != {python}>'.format(**locals())
        failures += 1
print
if failures == 0:
    print "Success!"
else:
    print "Failure: {} errors".format(failures)
