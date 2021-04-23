
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter
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
    y1=tupleData[1]
    y2=tupleData[2]
    y3=tupleData[3]

    p = figure(x_axis_label='time',
               y_axis_label='temperature',
               x_axis_type ='datetime')
    p.title = "simple line example"
    p.sizing_mode = "stretch_width"
    p.plot_height = 400
    p.xaxis.formatter = DatetimeTickFormatter(seconds=["%M:%S"],
                                            minutes=["%M:%S"],
                                            minsec=["%M:%S"],
                                            hours=["%M:%S"])

    p.line(x, y, legend_label='Temp1', line_width=2)
    curdoc().theme = 'dark_minimal'
    curdoc().add_root(p)
    script, div = components(p)

    return script, div, CDN.js_files


def bokeh_plot_all(listData):

    x = listData[0][0]
    y1=listData[0][1]
    y2=listData[1][1]
    y3=listData[2][2]

    p = figure(x_axis_label='time',
               y_axis_label='temperature',
               x_axis_type ='datetime')
    p.title = "simple line example"
    p.sizing_mode = "stretch_width"
    p.plot_height = 400
    p.xaxis.formatter = DatetimeTickFormatter(seconds=["%M:%S"],
                                            minutes=["%M:%S"],
                                            minsec=["%M:%S"],
                                            hours=["%M:%S"])

    p.line(x, y1, legend_label='Temp1', line_width=2)
    p.line(x, y2, legend_label='Temp2', line_width=2)
    p.line(x, y3, legend_label='Temp3', line_width=2)
    curdoc().theme = 'dark_minimal'
    curdoc().add_root(p)
    script, div = components(p)

    return script, div, CDN.js_files