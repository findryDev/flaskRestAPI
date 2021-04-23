
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import file_html


def bokeh_plot(tupleData):
    x = tupleData[0]
    y=tupleData[1]

    p = figure(title="simple line example",
            x_axis_label='x',
            y_axis_label='y',
            x_axis_type='datetime')

    p.line(x, y, legend_label='Temp1', line_width=2)

    html = file_html(p,CND, 'plot example')
    return html
