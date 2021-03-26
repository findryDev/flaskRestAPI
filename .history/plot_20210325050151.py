
from bokeh.plotting import figure, show

data = {'1': 7.0, '2': 19.0, '3': 18.0, '4': 37.0, '5': 29.0, '6': 23.0, '7': 18.0, '8': 6.0, '9': 11.0, '10': 34.0}




def bokeh_plot(data):


    y = list(data.keys())
    x = list(data.values())


    p = figure(title="simple line example",
            x_axis_label='x',
            y_axis_label='y')

    p.line(x, y, legend_label='Temp1', line_width=2)


    show(p)

bokeh_plot(data=data)