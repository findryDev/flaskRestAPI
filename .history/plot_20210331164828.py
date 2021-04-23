
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.io import curdoc
import datetime


data = ([datetime.datetime(2021, 3, 20, 19, 15, 6),
         datetime.datetime(2021, 3, 20, 19, 15, 42),
         datetime.datetime(2021, 3, 20, 19, 15, 56),
         datetime.datetime(2021, 3, 20, 19, 16, 11),
         datetime.datetime(2021, 3, 20, 19, 16, 26),
         datetime.datetime(2021, 3, 20, 19, 16, 38),
         datetime.datetime(2021, 3, 20, 19, 16, 51),
         datetime.datetime(2021, 3, 20, 19, 17, 6),
         datetime.datetime(2021, 3, 20, 19, 17, 21),
         datetime.datetime(2021, 3, 20, 19, 17, 36)],
        [7.0, 19.0, 18.0, 37.0, 29.0, 23.0, 18.0, 6.0, 11.0, 34.0])

def bokeh_plot(tupleData):
    x = tupleData[0]
    y=tupleData[1]

    p = figure(x_axis_label='x',
               y_axis_label='y',
               x_axis_type ='datetime')
    p.title = "simple line example"
    p.sizing_mode = "stretch_width"
    p.plot_height = 250
    p.line(x, y, legend_label='Temp1', line_width=2)
    curdoc().theme = 'dark_minimal'
    curdoc().add_root(p)
    script, div = components(p)

    return script, div, CDN.js_files
