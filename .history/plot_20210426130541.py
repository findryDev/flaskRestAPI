
from bokeh.core.enums import HorizontalLocation
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter, BoxAnnotation
from bokeh.plotting import reset_output
import pytz


local_tz = pytz.timezone('Europe/Warsaw')


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


def bokeh_plot(query, legend_label, title, color):
    reset_output()
    dates = []
    temperatures = []
    for m in query:
        dates.append(utc_to_local(m.Date))
        temperatures.append(m.temperature)
    dates, temperatures = reduceTimePause(dates, temperatures)
    lowBox = BoxAnnotation(top=30, fill_alpha=0.1, fill_color='blue')
    mediumBox = BoxAnnotation(bottom=30, top = 75, fill_alpha=0.1, fill_color='white')
    highBox = BoxAnnotation(bottom=75, top = 100, fill_alpha=0.1, fill_color='red')
    p = figure(x_axis_label='time',
               y_axis_label='temperature',
               x_axis_type='datetime')
    p.sizing_mode = 'scale_width'
    p.plot_height = 400
    p.xaxis.formatter = DatetimeTickFormatter(hours=["%H:%M"],
                                              minutes=["%H:%M"]
                                              )
    p.title.text = title
    p.title.text_font_size = "25px"
    p.xaxis.axis_label_text_font_size = "20px"
    p.yaxis.axis_label_text_font_size = "20px"
    p.line(dates, temperatures, legend_label=legend_label,
           line_width=2,
           color=color)

    curdoc().theme = 'dark_minimal'
    curdoc().add_root(p)
    script, div = components(p)
    return script, div


def bokeh_plots(queries, legend_labels, titles, colors):
    reset_output()
    x = []
    y = []
    for q in queries:

        queries.reverse()
        dates = []
        temperatures = []
        for m in q:
            dates.append(utc_to_local(m.Date))
            temperatures.append(m.temperature)
        dates, temperatures = reduceTimePause(dates, temperatures)
        if len(x) == 0:
            x.append(dates)
        y.append(temperatures)

    p = figure(x_axis_label='time',
               y_axis_label='temperature',
               x_axis_type='datetime')
    p.sizing_mode = 'scale_width'
    p.plot_height = 400
    p.xaxis.formatter = DatetimeTickFormatter(hours=["%H:%M"],
                                              minutes=["%H:%M"]
                                              )
    for i in range(len(y)):
        p.title.text = titles[i]
        p.title.text_font_size = "25px"
        p.xaxis.axis_label_text_font_size = "20px"
        p.yaxis.axis_label_text_font_size = "20px"
        p.line(x[0], y[i], legend_label=legend_labels[i],
               line_width=2,
               color=colors[i])

    curdoc().theme = 'dark_minimal'
    curdoc().add_root(p)
    script, div = components(p)
    return script, div


def CDN_js():
    return CDN.js_files
