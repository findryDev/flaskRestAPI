def bokeh_plot(data):
    from bokeh.plotting import figure, show


    x = [key for key in data.items()]
    y = [value for value in data.items()]


    p = figure(title="simple line example",
            x_axis_label='x',
            y_axis_label='y')

    p.line(x, y, legend_label='Temp1', line_width=2)


    show(p)