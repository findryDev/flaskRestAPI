
from bokeh.plotting import figure, show


def bokeh_plot(tupleData):
    x = tupleData[0]
    y=tupleData[1]

    p = figure(title="simple line example",
            x_axis_label='x',
            y_axis_label='y')

    p.line(x, y, legend_label='Temp1', line_width=2)


    show(p)
