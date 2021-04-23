
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter
import sqlalchemy
import datetime

def bokeh_plot(listOfModels, howMany, titles):
  x=[]
  y=[]
  for e in listOfModels:
    lastsElements = ((e.query.order_by(sqlalchemy.
                      desc(e.id)).limit(howMany).all()))
    lastsElements.reverse()
    dates = []
    temperatures = []
    for m in lastsElements:
      dates.append(m.Date)
      temperatures.append(m.temperature)
    if len(x) == 0: x.append(dates)
    y.append(temperatures)

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

  i = 0
  for e in y:
    p.line(x, e, legend_label=titles[i], line_width=2)
    i = i+1

  curdoc().theme = 'dark_minimal'
  curdoc().add_root(p)
  script, div = components(p)

  return script, div,

def CDN_js():
  return CDN.js_files