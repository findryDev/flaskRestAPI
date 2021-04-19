from bokeh.plotting import figure, show

x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]
y1 = [5, 6, 3, 1, 3]
y2 = [12, 27, 352, 44, 35]
y3 = [64, 74, 22, 42, 15]

p = figure(title="simple line example",
           x_axis_label='x',
           y_axis_label='y')
p.line(x, y, legend_label='Temp', line_width=2)
p.line(x, y1, legend_label='Temp1', line_width=2)
p.line(x, y2, legend_label='Temp2', line_width=2)
p.line(x, y3, legend_label='Temp3', line_width=2)


show(p)