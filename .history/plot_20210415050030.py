
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter
import sqlalchemy
import datetime


import pytz
local_tz = pytz.timezone('Europe/Warsaw') # use your local timezone name here
# NOTE: pytz.reference.LocalTimezone() would produce wrong result here
## You could use `tzlocal` module to get local timezone on Unix and Win32
# from tzlocal import get_localzone # $ pip install tzlocal
# # get local timezone
# local_tz = get_localzone()
def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary


def reduceTimePause(x, y):
    newListDate = []
    newListTemp = []

    newListStart = 0

    for i in range(len(x)-1):
        if (abs((x[i+1] - x[i]).total_seconds())) > 60*60*2:
            newListStart = i + 1

    for k in range(newListStart, len(x)):
        newListDate.append(x[k])
        newListTemp.append(y[k])

    return newListDate, newListTemp


def bokeh_plot(listOfModels, howMany, legend_labels, titles, colors):
    #correct time zone in labels
    x = []
    y = []
    for e in listOfModels:
        lastsElements = ((e.query.order_by(sqlalchemy.
                          desc(e.id)).limit(howMany).all()))
        lastsElements.reverse()
        dates = []
        temperatures = []
        for m in lastsElements:
            dates.append(m.Date)
            temperatures.append(m.temperature)
        dates, temperatures = reduceTimePause(dates, temperatures)

        if len(x) < howMany:
            x.append(dates)
        y.append(temperatures)

    p = figure(x_axis_label='time',
               y_axis_label='temperature',
               x_axis_type='datetime')
    p.sizing_mode = "stretch_width"
    p.plot_height = 400
    p.xaxis.formatter = DatetimeTickFormatter(hours=["%H:%M"],
                                              minutes=["%H:%M"]
                                              )
    i = 0
    xLocal = [utc_to_local(e) for e in x ]
    for e in y:
        p.title.text = titles
        p.title.text_font_size = "25px"
        p.xaxis.axis_label_text_font_size = "20px"
        p.yaxis.axis_label_text_font_size = "20px"
        p.line(x[0], e, legend_label=legend_labels[i],
               line_width=2,
               color=colors[i])
        i += 1

    '''
    if len(listOfModels) == 1:
        p.line(x[0], y[0], legend_label=titles[0], line_width=2)
    elif len(listOfModels) == 2:
        p.line(x[0], y[0], legend_label=titles[0], line_width=2)
        p.line(x[0], y[1], legend_label=titles[0], line_width=2)
    elif len(listOfModels) == 3:
        p.line(x[0], y[0], legend_label=titles[0], line_width=2)
        p.line(x[0], y[1], legend_label=titles[1], line_width=2)
        p.line(x[0], y[2], legend_label=titles[2], line_width=2)
    '''
    curdoc().theme = 'dark_minimal'
    curdoc().add_root(p)
    script, div = components(p)

    return script, div


def CDN_js():
    return CDN.js_files

