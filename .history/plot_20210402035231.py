
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter
import sqlalchemy
import datetime



models = [TemperatureModelSensor1, TemperatureModelSensor2, TemperatureModelSensor3]

def getLastRecordsToPlotDataAllModels(tempModels, howMany):
    allData = []
    for tempModel in tempModels:
        temperatureLast = ((tempModel.query.order_by(sqlalchemy.
                                desc(tempModel.id)).limit(howMany).all()))
        temperatureLast.reverse()
        x = []
        y = []
        for m in temperatureLast:
            x.append(m.Date)
            y.append(m.temperature)
        allData.append((x,y))

    return allData


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

    return script, div, CDN.js_files


def bokeh_plot_all(listData):

    x = listData[0][0]
    y1=listData[0][1]
    y2=listData[1][1]
    y3=listData[2][2]

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

    p.line(x, y1, legend_label='Temp1', line_width=2)
    p.line(x, y2, legend_label='Temp2', line_width=2)
    p.line(x, y3, legend_label='Temp3', line_width=2)
    curdoc().theme = 'dark_minimal'
    curdoc().add_root(p)
    script, div = components(p)

    return script, div, CDN.js_files


