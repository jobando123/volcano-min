import json
import matplotlib.pyplot as plt

OFFSET = 0.05       # offset for axis limits
# matplotlib doesn't allow setting image resolution (however, it offers setting the size in inches)
WIDTH_IN, HEIGHT_IN = 10, 7
DASHES = [5, 5]     # 8 dots for dash, 6 dots for space
COLOR = 'blue'

# Draw four lines (and form a box). All points inside this region will be
# (scatter-)plotted, whereas those outside will be handed over to HTML
RECT_X_MIN = -0.5
RECT_Y_MIN = None       # setting 'None' extends the edge to the frame
RECT_X_MAX = 0.5
RECT_Y_MAX = 1.5
RECT_OFFSET = 2 * OFFSET    # so that the edges lying over the axes are out of the picture

x, y = [], []
x_neg, y_neg = [], []
obj = {
    'names': [],
    'x': [],
    'y': [],
}

# CSV format: name,x,y
with open('voldat.csv', 'r') as fd:
    next(fd)
    min_x, min_y, max_x, max_y = float('inf'), float('inf'), float('-inf'), float('-inf')

    for line in fd:
        data = iter(line.split(','))
        name = next(data)
        x_ = float(next(data))
        y_ = float(next(data))

        if (RECT_X_MIN is not None and x_ < RECT_X_MIN) or \
           (RECT_X_MAX is not None and x_ > RECT_X_MAX) or \
           (RECT_Y_MIN is not None and y_ < RECT_Y_MIN) or \
           (RECT_Y_MAX is not None and y_ > RECT_Y_MAX):
            obj['names'].append(name)
            x_neg.append(x_)
            y_neg.append(y_)

        x.append(x_)
        y.append(y_)

        if x_ < min_x:
            min_x = x_
        if x_ > max_x:
            max_x = x_
        if y_ < min_y:
            min_y = y_
        if y_ > max_y:
            max_y = y_


fig, ax = plt.subplots()

# Initial scatter plot
ax.set_xlim([min_x - OFFSET, max_x + OFFSET])
ax.set_ylim([min_y - OFFSET, max_y + OFFSET])
ax.scatter(x, y, c=COLOR)

fig.set_size_inches(WIDTH_IN, HEIGHT_IN)

# form the rectangle
x_0 = (min_x - RECT_OFFSET) if RECT_X_MIN is None else RECT_X_MIN
x_1 = (max_x + RECT_OFFSET if RECT_X_MAX is None else RECT_X_MAX)
y_0 = (min_y - RECT_OFFSET) if RECT_Y_MIN is None else RECT_Y_MIN
y_1 = (max_y + RECT_OFFSET) if RECT_Y_MAX is None else RECT_Y_MAX

ax.plot((x_0, x_0, x_1, x_1, x_0), (y_0, y_1, y_1, y_0, y_0), c=COLOR)

# dashed lines
off = RECT_OFFSET + OFFSET      # just to keep it farther
ax.plot((x_0, x_0), (min_y - off, y_0), dashes=DASHES, c=COLOR)
ax.plot((x_0, x_0), (y_0, max_y + off), dashes=DASHES, c=COLOR)
ax.plot((x_1, x_1), (y_1, max_y + off), dashes=DASHES, c=COLOR)
ax.plot((x_1, x_1), (y_0, min_y - off), dashes=DASHES, c=COLOR)
ax.plot((min_x - off, x_0), (y_0, y_0), dashes=DASHES, c=COLOR)
ax.plot((min_x - off, x_0), (y_1, y_1), dashes=DASHES, c=COLOR)
ax.plot((x_1, max_x + off), (y_1, y_1), dashes=DASHES, c=COLOR)
ax.plot((x_1, max_x + off), (y_0, y_0), dashes=DASHES, c=COLOR)

width, height = fig.canvas.get_width_height()

# get the pixels corresponding to the collected points
for pts in zip(x_neg, y_neg):
    x_, y_ = ax.transData.transform(pts)
    obj['x'].append(x_)
    obj['y'].append(height - y_)    # invert the height (since it's calculated from top-left in HTML)

fig.savefig('plot.png', dpi=fig.dpi)    # should be the same as the figure's dpi

with open('gen.js', 'w') as fd:
    data = 'var obj = %s;' % json.dumps(obj, indent=2)
    fd.write(data)
