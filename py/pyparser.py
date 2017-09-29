# classes
from pyparsing import Combine, Literal, CaselessLiteral, Word, Optional, OneOrMore, Or, Group, Dict, ParseException
# variables
from pyparsing import nums
# functions
from pyparsing import srange

point = Literal('.')
e = CaselessLiteral('E')
plusorminus = Literal('+') | Literal('-')
number = Word(nums)
integer = Combine( Optional(plusorminus) + number )
floatnumber = Combine( integer +
                       Optional( point + Optional(number) ) +
                       Optional( e + integer )
                       )

timestamp = floatnumber
timestamp.setParseAction(lambda t: float(t[0]))
variable = Word(srange("[a-zA-Z_]"))
memSize = number + Literal("b").suppress()

singleValue = number
singleValue.setParseAction(lambda t: int(t[0]))
dictValue = Literal(":").suppress() + Dict(OneOrMore(Group(variable + memSize + Literal(";").suppress())))

line_parser = floatnumber + Word("info").suppress() + variable + (singleValue ^ dictValue)
