from bokeh.plotting import figure, show

x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

p = figure(title="simple line example",
           x_axis_lable='x',
           y_axis_lable='y')
p.line(x, y, legend_label='Temp', line_width=2)
show(p)