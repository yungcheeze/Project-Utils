import numpy as np
import matplotlib.pyplot as plt
import pprint as pp


# classes
from pyparsing import Combine, Literal, CaselessLiteral, Word, Optional, OneOrMore, Or, Group, Dict
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

# print(floatnumber.searchString(" hi 33.45 my 7.2 friend"))
# print(variable.searchString("winning when_is it EveR_not_Bad"))


test_lines = [ "0.0124178    info         constructor: size 5760b; ",
               "0.0124438    info         numObj 1    ",
               "0.0124547    info         total_mem 5760",
               "0.012465     info         shrink_to_fit: old_size 5760b; old_capacity 5760b; new_size 5760b; new_capacity 5760b; ",
               "0.0124764    info         reserve: old_size 5760b; old_capacity 5760b; new_size 5760b; new_capacity 5760b; "]


line_parser = floatnumber + Word("info").suppress() + variable + (singleValue ^ dictValue)

# for line in file("../results/MemoryAnalysis/totals_9-9-17_2232.log"):
lines = []
for line in test_lines:
    lines.append(line_parser.searchString(line)[0])


pp.pprint(lines)
# t1 = np.arange(0.0, 5.0, 0.1)
# t2 = np.arange(0.0, 10.0, 0.2)

# plt.plot(t1, t2, 'k')
# plt.show()
# nums = [ [0.0124178, "hi"],
#          [0.0124438, "man"],
#          [0.0124547, "does"],
#          [0.012465, "go"],
#          [0.0124764, "win"]]

# print(map(lambda t: t[0], nums))
