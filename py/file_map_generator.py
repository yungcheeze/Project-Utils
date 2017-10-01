import numpy as np
import re

lin_exp = r"""
        (?:\s*)                            # ignore potential whitespace
        (?P<timestamp>\b\d+(?:\.\d+)?\b)                 # 1: match timestamp
        (?:\s*)                            # ignore potential whitespace
        (?P<level>\binfo|debug\b)                   # 2: match log type
        (?:\s*)                            # ignore potential whitespace
        (?P<key_stmt>\b\w+\b)                          # 3: get key-stmt
        (?:
            (?::(?P<dict_vals>(?:\s \b\w+\b \s \b\d+b?;)+)) # 4: get dict suffix
            |                              # or
            (?: \s (?P<single_val>\b\d+\b))              # 5: get single val
        )
"""

r = re.compile(lin_exp, re.X)


entries = {}
log_file = file("../../results/Mem_Analysis_2/filtered_28-09-17_1720.log")

print("parsing logfile")
for i, line in enumerate(log_file):
    linum = i + 1
    if i % 500000 == 0:
        print " ".join(map(str, ("line", linum)))

    try:
        key = r.match(line).group("key_stmt")
        if key not in entries:
            entries[key] = []
        entries[key].append(linum)
    except AttributeError:
        if "eof" not in line:
            print line
            print linum
            print r.match(line).groups
            quit()


print("parsing complete")
print("saving to npz")

np.savez("parsed_filtered_28-09-17_1720", entries=entries)

print("save complete")
