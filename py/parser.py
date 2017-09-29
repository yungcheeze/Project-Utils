import numpy as np
import re


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
