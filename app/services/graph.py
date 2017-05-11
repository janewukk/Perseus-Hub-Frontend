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

import copy

import numpy as np

"""
Make a graph from a dataset file (PD compatible)

Notice: dataset should be in the Django root data/ folder
"""
def graph_from_file(dataset_filename):

    data = pd.read_table('data/' + dataset_filename, skipinitialspace=True, escapechar="\\")
    color_mapper = LinearColorMapper(palette=palette)

    source_true = ColumnDataSource(
        data =dict(
            x1=data['1'],
            y1=data['2'],
            color1=data['3'],
            x2=data['4'],
            y2=data['5'],
            color2=data['6'],
            x3=data['7'],
            y3=data['8'],
            color3=data['9']
        )
    )

    s_data = source_true.data

    source = ColumnDataSource(
        data =dict(
            x1=s_data['x1'],
            y1=s_data['y1'],
            color1=s_data['color1'],
            x2=s_data['x2'],
            y2=s_data['y2'],
            color2=s_data['color2'],
            x3=s_data['x3'],
            y3=s_data['y3'],
            color3=s_data['color3']
        )
    )

    xdr1 = DataRange1d("x1")
    ydr1 = DataRange1d("y1")
    xdr2 = DataRange1d("x2")
    ydr2 = DataRange1d("y2")
    xdr3 = DataRange1d("x3")
    ydr3 = DataRange1d("y3")
    window_size = 350
    between_window_size = 40
    border_size = 6

    def make_plot(xname, yname, xcolor, xdr, ydr, xax=False, yax=False):
        mbl = between_window_size if yax else 0
        mbb = between_window_size if xax else 0
        plot = figure(
            x_range=xdr, y_range=ydr, background_fill_color="white",
            border_fill_color='white', plot_width=window_size + mbl, plot_height=window_size + mbb,
            min_border_left=border_size+mbl, min_border_right=border_size, min_border_top=border_size, min_border_bottom=2+mbb,
            y_axis_type="log", x_axis_type="log")
        
        circle = Circle(x=xname, y=yname, fill_color={'field': xcolor, 'transform': color_mapper}, fill_alpha=0.6, size=5, line_color=None)
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

        plot.add_tools(BoxZoomTool(), WheelZoomTool(), PanTool(), ResetTool(), BoxSelectTool(), TapTool(), HoverTool())
        plot.xgrid.grid_line_color = None
        plot.ygrid.grid_line_color = None

        return plot

    xattrs = ["x1", "x2", "x3"]
    yattrs = ["y1", "y2", "y3"]
    plots = []

    row = []
    plot1 = make_plot("x1", "y1", "color1", xdr1, ydr1)
    plot2 = make_plot("x2", "y2", "color2", xdr2, ydr2)
    plot3 = make_plot("x3", "y3", "color3", xdr3, ydr3)
    row.append(plot1)
    row.append(plot2)
    row.append(plot3)
    plots.append(row)

    stats = Div(text='', width=9000)

    # Tickers
    ticker1x = Select(title="x1-axis:", value="x1", options=["x1", "x2", "x3", "y1", "y2", "y3"])
    ticker1y = Select(title="y1-axis:", value="y1", options=["x1", "x2", "x3", "y1", "y2", "y3"])

    ticker2x = Select(title="x2-axis:", value="x2", options=["x1", "x2", "x3", "y1", "y2", "y3"])
    ticker2y = Select(title="y2-axis:", value="y2", options=["x1", "x2", "x3", "y1", "y2", "y3"])

    ticker3x = Select(title="x3-axis:", value="x2", options=["x1", "x2", "x3", "y1", "y2", "y3"])
    ticker3y = Select(title="y3-axis:", value="y2", options=["x1", "x2", "x3", "y1", "y2", "y3"])

    tickers_rowx = bokeh.layouts.row(ticker1x, ticker2x, ticker3x)
    tickers_rowy = bokeh.layouts.row(ticker1y, ticker2y, ticker3y)

    plots_row = gridplot(plots)
    layout = bokeh.layouts.column(tickers_rowx, tickers_rowy, plots_row, stats, sizing_mode='scale_width')

    callback_ticker1x = CustomJS(args=dict(source=source, source_true=source_true), code="""
        console.log("Callback_ticker1x is called");
        var value = cb_obj.get("value");
        source['data']['x1'] = source_true['data'][value];
        source.trigger('change')
    """)

    callback_ticker1y = CustomJS(args=dict(source=source, source_true=source_true), code="""
        console.log("Callback_ticker1y is called");
        var value = cb_obj.get("value");
        source['data']['y1'] = source_true['data'][value];
        source.trigger('change')
    """)

    callback_ticker2x = CustomJS(args=dict(source=source, source_true=source_true), code="""
        console.log("Callback_ticker2x is called");
        var value = cb_obj.get("value");
        source['data']['x2'] = source_true['data'][value];
        source.trigger('change')
    """)

    callback_ticker2y = CustomJS(args=dict(source=source, source_true=source_true), code="""
        console.log("Callback_ticker2y is called");
        var value = cb_obj.get("value");
        source['data']['y2'] = source_true['data'][value];
        source.trigger('change')
    """)

    callback_ticker3x = CustomJS(args=dict(source=source, source_true=source_true), code="""
        console.log("Callback_ticker3x is called");
        var value = cb_obj.get("value");
        source['data']['x3'] = source_true['data'][value];
        source.trigger('change')
    """)

    callback_ticker3y = CustomJS(args=dict(source=source, source_true=source_true), code="""
        console.log("Callback_ticker3y is called");
        var value = cb_obj.get("value");
        source['data']['y3'] = source_true['data'][value];
        source.trigger('change')
    """)

    callback = CustomJS(args=dict(source=source, stats=stats), code="""
        console.log("Selected callback was called");
        var inds = cb_obj.selected['1d'].indices;
        
        // call the frontend custom js function defined in dataset-template.html
        nodeSelected(inds);

        // Clear the table
        stats.text = '';
        stats.text += `<table class="graph-stats-table">
                        <tr>
                            <th>ID</th>
                            <th>x1</th>
                            <th>y1</th>
                            <th>x2</th>
                            <th>y2</th>
                            <th>x3</th>
                            <th>y3</th>
                        </tr>`

        for (i = 0; i < inds.length; i++) {
                var id = inds[i];
                var x1 = source['data']['x1'][id];
                var y1 = source['data']['y1'][id];
                var x2 = source['data']['x2'][id];
                var y2 = source['data']['y2'][id];
                var x3 = source['data']['x3'][id];
                var y3 = source['data']['y3'][id];
                stats.text += "<tr><td>"+String(id)+"</td>"
                + "<td>"+String(x1)+"</td>"
                + "<td>"+String(y1)+"</td>"
                + "<td>"+String(x2)+"</td>"
                + "<td>"+String(y2)+"</td>"
                + "<td>"+String(x3)+"</td>"
                + "<td>"+String(y3)+"</td>"+"</tr>";
        }
        stats.text += "</table>"
                    
        // console.log(source);
        // console.log(inds);
    """)

    source.js_on_change('selected', callback)

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
