import numpy as np
import matplotlib.pyplot as plt
# import pprint as pp

print("loading files")

data = np.load("./parsed_logfile.npz")

print(data.files)

lines = data['lines']
entries = data['entries'].item()


def color_y_axis(ax, color):
    """Color your axes."""
    for t in ax.get_yticklabels():
        t.set_color(color)
    return None


def b_to_mb(val):
    return val / 1000000


def total_mem_y():
    global lines
    global entries
    for i in entries.get("total_mem"):
        yield b_to_mb(lines[i][2])  # memory Usage


def plot_timestamp(indices):
    global lines
    for i in indices:
        yield lines[i][0]  # timestamp


def plot_constructor_alloc():
    global lines
    global entries
    for i in entries.get("constructor"):
        yield lines[i]["size"]


print("init plots")

fig, ax = plt.subplots()

h1, = ax.plot(list(plot_timestamp(entries["total_mem"])), list(total_mem_y()), 'r', label="total memory allocated")
ax.set_xlabel("time(s)")
ax.set_ylabel("megabytes")

ax2 = ax.twinx()
h2, = ax2.plot(list(plot_timestamp(entries["constructor"])), list(plot_constructor_alloc()), 'b', label="memory allocated by call to constructor")
ax2.set_ylim([0, 20000])
ax2.set_ylabel("bytes")

color_y_axis(ax, 'r')
color_y_axis(ax2, 'b')

ax.legend(loc='upper left', handles=[h1, h2])
print("finished")
