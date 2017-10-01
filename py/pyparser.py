import re
import linecache

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

line_pattern = re.compile(lin_exp, re.X)

dict_exp = r"""
        (?:
            \s
            (?P<key>\b\w+\b)  # key
            \s
            (?P<value>\b\d+)b?  # value
        ;)
"""

dict_pattern = re.compile(dict_exp, re.X)


def get_line_val(filename, linum, stmt_key):
    global line_pattern
    line = linecache.getline(filename, linum)
    match = line_pattern.match(line)
    try:
       val = match.group(stmt_key)
       return val
    except AttributeError:
        print("line", linum, line)
        return "-1"



def get_dict_val(filename, linum, dict_key):
    line = linecache.getline(filename, linum)
    pattern = gen_dict_val_exp(dict_key)
    match = pattern.search(line)
    return match.group("value")


def get_dict(filename, linum):
    global line_pattern
    global dict_pattern
    line = linecache.getline(filename, linum)
    match = line_pattern.match(line)
    dict_string = match.group("dict_vals")
    dict_tuples = dict_pattern.findall(dict_string)
    print dict_tuples
    return dict(dict_tuples)


def gen_dict_val_exp(dict_key):
    # dict_exp = r"\b"
    # + re.escape(dict_key)
    # + r"\b"
    # + r"\s(?P<value>\b\d+)"
    dict_exp = r"\b" + re.escape(dict_key) + r"\b" + r"\s(?P<value>\b\d+)"
    return re.compile(dict_exp)
