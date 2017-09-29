import numpy as np
import re


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

r = re.compile(r"\s*(\d+(\.\d*)?)\s*(\w+)\s*(\w+)")


entries = {}
log_file = file("../../results/Mem_Analysis_2/filtered_28-09-17_1720.log")

print("parsing logfile")
for i, line in enumerate(log_file):
    if i % 500000 == 0:
        print " ".join(map(str, ("line", i)))

    try:
        key = r.match(line).group(4)
        if key not in entries:
            entries[key] = []
        entries[key].append(i)
    except ParseException:
        continue
    except AttributeError:
        if "eof" not in line:
            print line
            print i
            print r.match(line).groups
            quit()


print("parsing complete")
print("saving to npz")

np.savez("parsed_filtered_28-09-17_1720", entries=entries)

print("save complete")
