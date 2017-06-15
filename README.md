## volcano-min

As useful as they are, [volcano plots](https://en.wikipedia.org/wiki/Volcano_plot_(statistics)) often take **huge** data input, which means plotting them in a webpage will result in generating thousands (or probably millions) of HTML elements for the data points (which is usually an overkill for your browser). This was an attempt to *work around* this problem.

Volcano plots have a crowded area where most of the points (at least 80% of a sample) will be located. People are usually interested in the points that lie **outside this crowded area** (i.e., which show large deviation). So, the idea is to isolate those points of interest from the bulk.

We initially generate the scatter plot (in PNG format) using python's [matplotlib](http://matplotlib.org/), define boundaries for a (rectangular) container, get the coordinates of points outside this region and generate a JSON data. This is then loaded into the webpage, and `div` elements (points) are distributed relative to the plot using these coordinates (much like image mapping). Hovering over a point shows a tooltip, which can have the details about the point (in this case, it's the "name" obtained from the CSV, but you can tweak around).

### Usage

- Make sure that you have matplotlib.
- Set the rectangle's boundaries in `volcano.py` (setting a value to `None` extends the corresponding edge to the adjacent frame's edge).
- Run `python volcano.py` to generate `plot.png` and `gen.js`
- Open `index.html` to see the changes ([working demo](http://wafflespeanut.github.io/volcano-min)).
