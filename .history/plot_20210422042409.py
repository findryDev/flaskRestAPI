<<<<<<< HEAD

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter
import sqlalchemy


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


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


def bokeh_plot(queries, legend_labels, titles, colors):
    x = []
    y = []
    queries.reverse()
        dates = []
        temperatures = []
        for m in lastsElements:
            dates.append(utc_to_local(m.Date))
            temperatures.append(m.temperature)
        dates, temperatures = reduceTimePause(dates, temperatures)

        if len(x) <= howMany:
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
    for e in listOfModels:


    return script, div


def CDN_js():
    return CDN.js_files
=======

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter
import sqlalchemy


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


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


def bokeh_plot(queries, legend_labels, titles, colors):
    x = []
    y = []
    queries.reverse()
        dates = []
        temperatures = []
        for m in lastsElements:
            dates.append(utc_to_local(m.Date))
            temperatures.append(m.temperature)
        dates, temperatures = reduceTimePause(dates, temperatures)

        if len(x) <= howMany:
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
    for e in listOfModels:


    return script, div


def CDN_js():
    return CDN.js_files
>>>>>>> 0b75138e047af14274c183f7e76284f83985dc5d
