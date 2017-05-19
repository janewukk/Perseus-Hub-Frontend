from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

from bokeh.charts import Histogram
from bokeh.sampledata.iris import flowers as data

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import autoload_server
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, CustomJS, LinearColorMapper
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.layouts import gridplot, widgetbox, row, column, layout
from bokeh.models.widgets import Button, PreText, Paragraph, Div, Select
from bokeh.models.glyphs import Circle
from bokeh.models import (BasicTicker, ColumnDataSource, Grid, LinearAxis,
                         DataRange1d, PanTool, Plot, WheelZoomTool, BoxZoomTool,ResetTool, BoxSelectTool, TapTool, HoverTool)
import bokeh.layouts
from bokeh.resources import INLINE
from bokeh.sampledata.iris import flowers
from bokeh.util.browser import view
from bokeh.plotting import *
from bokeh.io import curdoc
import pandas as pd
pd.set_option('display.max_rows', 5000000)
import json
import datetime

from bokeh.client import push_session

from tornado.ioloop import IOLoop
from bokeh.palettes import Plasma11 as palette

from bokeh.events import Tap, Press

import copy

import numpy as np

"""
Make a graph from a dataset file (PD compatible)

Notice: dataset should be in the Django root data/ folder
"""
def graph_from_file(dataset_filename):

    data = pd.read_csv('data/' + dataset_filename, skipinitialspace=True, escapechar="\\", header=None)
    color_mapper = LinearColorMapper(palette=palette)

    source_true = ColumnDataSource(
        data =dict(
            v1=data[4],
            v2=data[5],
            v3=data[6],
            v4=data[7],
            v5=data[8],
            v6=data[9],
            v7=data[10],
            v8=data[11],
            v9=data[12],
            v10=data[13]
        )
    )

    source_state = ColumnDataSource(
        data = dict(
            state = [1]
        )
    )

    s_data = source_true.data

    source = ColumnDataSource(
        data =dict(
            degree=data[0],
            count=data[1],
            pagerank=data[2],
            pagerank_count=data[3],
            v1=s_data['v1'],
            v2=s_data['v2'],
            v3=s_data['v3'],
            v4=s_data['v4'],
            v5=s_data['v5'],
            v6=s_data['v6']
        )
    )

    degree_x_p1 = DataRange1d("degree")
    degree_x_p2 = DataRange1d("degree")
    count_y = DataRange1d("count")
    pagerank_y = DataRange1d("pagerank")
    pagerank_x = DataRange1d("pagerank")
    pagerank_count = DataRange1d("pagerank_count")

    p4_x = DataRange1d("v1")
    p4_y = DataRange1d("v2")
    p5_x = DataRange1d("v3")
    p5_y = DataRange1d("v4")
    p6_x = DataRange1d("v5")
    p6_y = DataRange1d("v6")

    # v4 = DataRange1d("v4")
    # v5 = DataRange1d("v5")
    # v6 = DataRange1d("v6")
    # v7 = DataRange1d("v7")
    # v8 = DataRange1d("v8")
    # v9 = DataRange1d("v9")

    window_size = 350
    between_window_size = 40
    border_size = 6

    def make_plot(xname, yname, isLog, needsColor, xcolor, xdr, ydr, xax=False, yax=False):
        mbl = between_window_size if yax else 0
        mbb = between_window_size if xax else 0

        if isLog:
            plot = figure(
                x_range=xdr, y_range=ydr, background_fill_color="white",
                border_fill_color='white', plot_width=window_size + mbl, plot_height=window_size + mbb,
                min_border_left=border_size+mbl, min_border_right=border_size, min_border_top=border_size, min_border_bottom=2+mbb,
                y_axis_type="log", x_axis_type="log")
        else:
            plot = figure(
                x_range=xdr, y_range=ydr, background_fill_color="white",
                border_fill_color='white', plot_width=window_size + mbl, plot_height=window_size + mbb,
                min_border_left=border_size+mbl, min_border_right=border_size, min_border_top=border_size, min_border_bottom=2+mbb)

        plot.xaxis.axis_label = xname
        plot.yaxis.axis_label = yname
        
        if needsColor:
            circle = Circle(x=xname, y=yname, fill_color={'field': xcolor, 'transform': color_mapper}, fill_alpha=0.6, size=5, line_color=None)
        else:
            circle = Circle(x=xname, y=yname, fill_color = "blue", fill_alpha=0.6, size=5, line_color=None)

        r = plot.add_glyph(source, circle)
        r.nonselection_glyph = Circle(fill_color="grey", fill_alpha = 0.1, line_color=None)

        xdr.renderers.append(r)
        ydr.renderers.append(r)

        xticker = BasicTicker()
        if xax:
            xaxis = LinearAxis(axis_label=xname)
            plot.add_layout(xaxis, 'below')
            xticker = xaxis.ticker
        plot.add_layout(Grid(dimension=0, ticker=xticker))

        yticker = BasicTicker()
        if yax:
            yaxis = LinearAxis(axis_label=yname)
            plot.add_layout(yaxis, 'left')
            yticker = yaxis.ticker
        plot.add_layout(Grid(dimension=1, ticker=yticker))

        plot.add_tools(BoxZoomTool(), WheelZoomTool(), PanTool(), ResetTool(), BoxSelectTool(), TapTool())
        plot.xgrid.grid_line_color = None
        plot.ygrid.grid_line_color = None

        return plot


    # plots_row1 = []
    # row = []

    plot1 = make_plot("degree", "count", True, False, "", degree_x_p1, count_y)
    plot2 = make_plot("degree", "pagerank", True, True, "pagerank_count", degree_x_p2, pagerank_y)
    plot3 = make_plot("pagerank", "pagerank_count", True, False, "", pagerank_x, pagerank_count)

    # row.append(plot1)
    # row.append(plot2)
    # row.append(plot3)
    # plots_row1.append(row)

    # plots_row2 = []
    # row = []

    plot4 = make_plot("v1", "v2", False, False, "", p4_x, p4_y)
    plot5 = make_plot("v3", "v4", False, False, "", p5_x, p5_y)
    plot6 = make_plot("v5", "v6", False, False, "", p6_x, p6_y)

    # row.append(plot4)
    # row.append(plot5)
    # row.append(plot6)
    # plots_row2.append(row)


    stats = Div(text='', width=9000)

    # Tickers
    ticker1x = Select(title="x1-axis:", value="v1", options=["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10"])
    ticker1y = Select(title="y1-axis:", value="v2", options=["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10"])
    ticker2x = Select(title="x2-axis:", value="v3", options=["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10"])
    ticker2y = Select(title="y2-axis:", value="v4", options=["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10"])
    ticker3x = Select(title="x3-axis:", value="v5", options=["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10"])
    ticker3y = Select(title="y3-axis:", value="v6", options=["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10"])

    tickers_rowx = bokeh.layouts.row(ticker1x, ticker2x, ticker3x)
    tickers_rowy = bokeh.layouts.row(ticker1y, ticker2y, ticker3y)

    plots_row = gridplot([[plot1, plot2, plot3],[plot4, plot5, plot6]])

    layout = bokeh.layouts.column(tickers_rowx, tickers_rowy, plots_row, stats, sizing_mode='scale_width')

    callback_ticker1x = CustomJS(args=dict(source=source, source_true=source_true, plot=plot4), code="""
        console.log("Callback_ticker1x is called");
        var value = cb_obj.get("value");
        source['data']['v1'] = source_true['data'][value];
        plot.below[0].axis_label = value;
        source.trigger('change')
    """)

    callback_ticker1y = CustomJS(args=dict(source=source, source_true=source_true, plot=plot4), code="""
        console.log("Callback_ticker1y is called");
        var value = cb_obj.get("value");
        source['data']['v2'] = source_true['data'][value];
        plot.left[0].axis_label = value;
        source.trigger('change')
    """)

    callback_ticker2x = CustomJS(args=dict(source=source, source_true=source_true,plot=plot5), code="""
        console.log("Callback_ticker2x is called");
        var value = cb_obj.get("value");
        source['data']['v3'] = source_true['data'][value];
        plot.below[0].axis_label = value;
        source.trigger('change')
    """)

    callback_ticker2y = CustomJS(args=dict(source=source, source_true=source_true,plot=plot5), code="""
        console.log("Callback_ticker2y is called");
        var value = cb_obj.get("value");
        source['data']['v4'] = source_true['data'][value];
        plot.left[0].axis_label = value;
        source.trigger('change')
    """)

    callback_ticker3x = CustomJS(args=dict(source=source, source_true=source_true, plot=plot6), code="""
        console.log("Callback_ticker3x is called");
        var value = cb_obj.get("value");
        source['data']['v5'] = source_true['data'][value];
        plot.below[0].axis_label = value;
        source.trigger('change')
    """)

    callback_ticker3y = CustomJS(args=dict(source=source, source_true=source_true, plot=plot6), code="""
        console.log("Callback_ticker3y is called");
        var value = cb_obj.get("value");
        source['data']['v6'] = source_true['data'][value];
        plot.left[0].axis_label = value;
        source.trigger('change')
    """)

    callback = CustomJS(args=dict(source=source, source_new=source_state, stats=stats,
        tk1x=ticker1x, tk1y=ticker1y, tk2x=ticker2x, tk2y=ticker2y, tk3x=ticker3x, tk3y=ticker3y), code="""
        console.log("Selected callback was called");
        var inds = cb_obj.selected['1d'].indices;
        state = Number(source_new['data']['state'][0])
        console.log("State is:", state)

        var name = ['degree', 'count', 'pagerank', 'pagerank_count', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6']

        // Update the right names for the eigenvectors
        if (state >= 4 && state <= 6) {
            if (state === 4) {
                name[4] = tk1x.get("value");
                name[5] = tk1y.get("value");
            }
            else if (state === 5) {
                name[6] = tk2x.get("value");
                name[7] = tk2y.get("value");
            }
            else if (state === 6) {
                name[8] = tk3x.get("value");
                name[9] = tk3y.get("value");
            }
        }

        console.log(name);

        var x1 = source['data'][name[2*state-2]][inds[0]];
        var y1 = source['data'][name[2*state-1]][inds[0]];
        nodeSelected(x1, y1)
    """)

    event_callback_1 = CustomJS(args=dict(source=source_state),code="""
        source['data']['state'] = [1];
        console.log(1111111)
    """)
    event_callback_2 = CustomJS(args=dict(source=source_state),code="""
        source['data']['state'] = [2];
        console.log(2222222)
    """)
    event_callback_3 = CustomJS(args=dict(source=source_state),code="""
        source['data']['state'] = [3];
        console.log(3333333)
    """)
    event_callback_4 = CustomJS(args=dict(source=source_state),code="""
        source['data']['state'] = [4];
        console.log(4444444)
    """)
    event_callback_5 = CustomJS(args=dict(source=source_state),code="""
        source['data']['state'] = [5];
        console.log(5555555)
    """)
    event_callback_6 = CustomJS(args=dict(source=source_state),code="""
        source['data']['state'] = [6];
        console.log(6666666)
    """)

    plot1.js_on_event(Tap, event_callback_1)
    plot1.js_on_event(Press, event_callback_1)
    plot2.js_on_event(Tap, event_callback_2)
    plot2.js_on_event(Press, event_callback_2)
    plot3.js_on_event(Tap, event_callback_3)
    plot3.js_on_event(Press, event_callback_3)
    plot4.js_on_event(Tap, event_callback_4)
    plot4.js_on_event(Press, event_callback_4)
    plot5.js_on_event(Tap, event_callback_5)
    plot5.js_on_event(Press, event_callback_5)
    plot6.js_on_event(Tap, event_callback_6)
    plot6.js_on_event(Press, event_callback_6)

    source.js_on_change("selected", callback)

    ticker1x.js_on_change('value', callback_ticker1x)
    ticker1y.js_on_change('value', callback_ticker1y)
    ticker2x.js_on_change('value', callback_ticker2x)
    ticker2y.js_on_change('value', callback_ticker2y)
    ticker3x.js_on_change('value', callback_ticker3x)
    ticker3y.js_on_change('value', callback_ticker3y)
 
    script, div = components(layout, CDN)

    return {
        "graph_script": script, 
        "graph": div
    }
