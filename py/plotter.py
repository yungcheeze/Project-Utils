import numpy as np
import matplotlib.pyplot as plt
from misc_funcs import make_format
from line_parser import get_line_val, get_dict_val


# Main Plotting Functions
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


def plot_custom(stmt_key, plotting_func):
    global entries
    global log_file_path
    for i in entries.get(stmt_key):
        val, is_valid = plotting_func(log_file_path, i)
        yield val


def color_y_axis(ax, color):
    """Color your axes."""
    for t in ax.get_yticklabels():
        t.set_color(color)
    return None


# Conversion Functions
def to_mb(val):
    val = float(val)
    return val / 1000000


# custom plotting functions
def plot_size_change(log_file_path, linum):
    old_size = int(get_dict_val(log_file_path, linum, "old_size"))
    new_size = int(get_dict_val(log_file_path, linum, "new_size"))
    change = new_size - old_size
    isValid = True if change != 0 else False
    return (change, isValid)


def plot_capacity_change(log_file_path, linum):
    old_capacity = int(get_dict_val(log_file_path, linum, "old_capacity"))
    new_capacity = int(get_dict_val(log_file_path, linum, "new_capacity"))
    change = new_capacity - old_capacity
    isValid = True if change != 0 else False
    return (change, isValid)


def print_value_analysis(func, stat, vals):
    print "value analysis: " + func + " " + stat
    zero_count, pos_count, neg_count = 0, 0, 0
    for v in vals:
        if v < 0:
            neg_count += 1
        elif v == 0:
            pos_count += 1
        else:
            pos_count += 1

    print ("negatives: ", neg_count)
    print ("positives: ", pos_count)
    print ("zeros: ", zero_count)



print("loading files")

data = np.load("./parsed_filtered_28-09-17_1720.npz")

print(data.files)

log_file_path = "../../results/Mem_Analysis_2/filtered_28-09-17_1720.log"
entries = data['entries'].item()

print "files loaded"


print("init plots")

fig, ax = plt.subplots()
ax.set_xlabel("time(s)")
ax.set_ylabel("megabytes")

x1 = list(plot_timestamp("total_capacity"))
y1 = list(plot_single_val("total_capacity", conversion_func=to_mb))
h1, = ax.plot(x1, y1, 'r', label="total memory allocated")
print "plot 1 complete"

x1_2 = list(plot_timestamp("total_size"))
y1_2 = list(plot_single_val("total_size", conversion_func=to_mb))
h1_2, = ax.plot(x1_2, y1_2, 'g--', label="total used memory")
print "plot 2 complete"

ax2 = ax.twinx()
ax2.set_ylabel("bytes")

x2 = list(plot_timestamp("constructor"))
y2 = list(plot_dict_val("constructor", "size"))
h2, = ax2.plot(x2, y2, 'bx', label="mem alloc constructor", linewidth=7)
print "plot 3 complete"

x2_1 = list(plot_timestamp("destructor"))
y2_1 = list(plot_dict_val("destructor", "mem_freed"))
h2_1, = ax2.plot(x2_1, y2_1, 'kx', label="mem free destructor", linewidth=7)
print "plot 4 complete"

x2_2 = list(plot_timestamp("resize"))
y2_2 = list(plot_custom("resize", plot_size_change))
h2_2, = ax2.plot(x2_2, y2_2, 'm_', label="resize: size change", linewidth=7)
print "plot 5 complete"

x2_3 = list(plot_timestamp("resize"))
y2_3 = list(plot_custom("resize", plot_capacity_change))
h2_3, = ax2.plot(x2_3, y2_3, 'c_', label="resize: capacity change", linewidth=7)
print "plot 6 complete"

x2_4 = list(plot_timestamp("shrink_to_fit"))
y2_4 = list(plot_custom("shrink_to_fit", plot_capacity_change))
h2_4, = ax2.plot(x2_4, y2_4, 'g_', label="shrink_to_fit: capacity change", linewidth=7)
print "plot 7 complete"

color_y_axis(ax, 'r')
color_y_axis(ax2, 'b')

ax2.format_coord = make_format(ax2, ax)

ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., handles=[h1, h1_2, h2, h2_1])
print("finished")
