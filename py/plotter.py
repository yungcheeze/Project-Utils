import numpy as np
import matplotlib.pyplot as plt
from pyparser import get_line_val, get_dict_val
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


def b_to_mb(val):
    return val / 1000000


def plot_single_val(stmt_key):
    global entries
    global log_file_path
    for i in entries.get(stmt_key):
        yield get_line_val(log_file_path, i, "single_val")


def plot_dict_val(stmt_key, dict_key):
    global entries
    global log_file_path
    for i in entries.get(stmt_key):
        yield get_dict_val(log_file_path, i, dict_key)


def plot_timestamp(stmt_key):
    global entries
    global log_file_path
    for i in entries.get(stmt_key):
        yield get_line_val(log_file_path, i, "timestamp")



print("init plots")

fig, ax = plt.subplots()

h1, = ax.plot(list(plot_timestamp("total_capacity")), list(plot_single_val("total_capacity")), 'r', label="total memory allocated")
print "plot 1 complete"
h1_2, = ax.plot(list(plot_timestamp("total_size")), list(plot_single_val("total_size")), 'g', label="total used memory (out of total allocated)")
print "plot 2 complete"
ax.set_xlabel("time(s)")
ax.set_ylabel("megabytes")

ax2 = ax.twinx()
h2, = ax2.plot(list(plot_timestamp("constructor")), list(plot_dict_val("constructor", "size")), 'b', label="memory allocated by call to constructor")
print "plot 3 complete"
ax2.set_ylim([0, 20000])
ax2.set_ylabel("bytes")

color_y_axis(ax, 'r')
color_y_axis(ax2, 'b')

ax.legend(loc='upper left', handles=[h1, h1_2, h2])
print("finished")
