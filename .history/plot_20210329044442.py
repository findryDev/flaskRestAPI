
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import components


def bokeh_plot(tupleData):
    x = tupleData[0]
    y=tupleData[1]

    p = figure(title="simple line example",
            x_axis_label='x',
            y_axis_label='y',
            x_axis_type='datetime')

    p.line(x, y, legend_label='Temp1', line_width=2)

    script, div = components(p)

    return script, div, CDN.css_components
