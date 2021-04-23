
from bokeh.plotting import figure, show

data = {'20-03-21 20:15:06': 7.0, '20-03-21 20:15:42': 19.0, '20-03-21 20:15:56': 18.0, '20-03-21 20:16:11': 37.0, '20-03-21 20:16:26': 29.0, '20-03-21 20:16:38': 23.0, '20-03-21 20:16:51': 18.0, '20-03-21 20:17:06': 6.0, '20-03-21 20:17:21': 11.0, '20-03-21 20:17:36': 34.0}




def bokeh_plot(data):


    x ,y = [key for key in data.items()]


    p = figure(title="simple line example",
            x_axis_label='x',
            y_axis_label='y')

    p.line(x, y, legend_label='Temp1', line_width=2)


    show(p)

bokeh_plot(data=data)