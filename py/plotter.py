import numpy as np
import matplotlib.pyplot as plt
from pyparser import get_line_val, get_dict_val
from misc_funcs import make_format
# import pprint as pp

print("loading files")

data = np.load("./parsed_filtered_28-09-17_1720.npz")

print(data.files)

log_file_path = "../../results/Mem_Analysis_2/filtered_28-09-17_1720.log"
# entries = data['entries'].item()

print "files loaded"


def color_y_axis(ax, color):
    """Color your axes."""
    for t in ax.get_yticklabels():
        t.set_color(color)
    return None


def to_mb(val):
    val = float(val)
    return val / 1000000


def plot_single_val(stmt_key, conversion_func=str):
    global entries
    global log_file_path
    for i in entries.get(stmt_key):
        yield conversion_func(get_line_val(log_file_path, i, "single_val"))


def plot_dict_val(stmt_key, dict_key, conversion_func=str):
    global entries
    global log_file_path
    for i in entries.get(stmt_key):
        yield conversion_func(get_dict_val(log_file_path, i, dict_key))


def plot_timestamp(stmt_key, conversion_func=str):
    global entries
    global log_file_path
    for i in entries.get(stmt_key):
        yield conversion_func(get_line_val(log_file_path, i, "timestamp"))



print("init plots")

fig, ax = plt.subplots()
ax.set_xlabel("time(s)")
ax.set_ylabel("megabytes")

# x1 = list(plot_timestamp("total_capacity"))
# y1 = list(plot_single_val("total_capacity", conversion_func=to_mb))
h1, = ax.plot(x1, y1, 'r', label="total memory allocated")
print "plot 1 complete"

# x1_2 = list(plot_timestamp("total_size"))
# y1_2 = list(plot_single_val("total_size", conversion_func=to_mb))
h1_2, = ax.plot(x1_2, y1_2, 'g', label="total used memory (out of total allocated)")
print "plot 2 complete"

ax2 = ax.twinx()
ax2.set_ylabel("bytes")

# x2 = list(plot_timestamp("constructor"))
# y2 = list(plot_dict_val("constructor", "size"))
h2, = ax2.plot(x2, y2, 'b_', label="memory allocated by call to constructor")
print "plot 3 complete"

color_y_axis(ax, 'r')
color_y_axis(ax2, 'b')

ax2.format_coord = make_format(ax2, ax)

ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., handles=[h1, h1_2, h2])
print("finished")
