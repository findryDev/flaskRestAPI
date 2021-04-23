
from bokeh.plotting import figure, show

data = {'a': 7.0, '2': 19.0, 'b': 18.0, 'c': 37.0, 'd': 29.0, 'e': 23.0, 'f': 18.0, 'g': 6.0, 'h': 11.0, 'i': 34.0}




def bokeh_plot(x,y):

    p = figure(title="simple line example",
            x_axis_label='x',
            y_axis_label='y')

    p.line(x, y, legend_label='Temp1', line_width=2)


    show(p)
