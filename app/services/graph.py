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
                         DataRange1d, PanTool, Plot, WheelZoomTool, BoxZoomTool,ResetTool,
                         BoxSelectTool, TapTool, HoverTool, LassoSelectTool)
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
import time 

"""
Make a graph from a dataset file (PD compatible)

Notice: dataset should be in the Django root data/ folder
"""

class Graph:
    def __init__(self):
        self.source = ColumnDataSource()
        self.highlightSource = ColumnDataSource
        self.highlighted = False
        self.highlightedNodeIDs = []

    def graph_from_file(self, dataset_filename):
        pd.set_option('display.precision',20)
        data = pd.read_csv('data/' + dataset_filename, skipinitialspace=True, escapechar="\\", header=None)
        data_string = pd.read_csv('data/' + dataset_filename, skipinitialspace=True, escapechar="\\", header=None, dtype=str)
        color_mapper = LinearColorMapper(palette=palette)


        source_true_string = ColumnDataSource(
            data =dict(
                v1=data_string[6],
                v2=data_string[7],
                v3=data_string[8],
                v4=data_string[9],
                v5=data_string[10],
                v6=data_string[11],
                v7=data_string[12],
                v8=data_string[13],
                v9=data_string[14],
                v10=data_string[15]
            )
        )

        source_true = ColumnDataSource(
            data =dict(
                v1=data[6],
                v2=data[7],
                v3=data[8],
                v4=data[9],
                v5=data[10],
                v6=data[11],
                v7=data[12],
                v8=data[13],
                v9=data[14],
                v10=data[15]
            )
        )

        source_state = ColumnDataSource(
            data = dict(
                state = [1],
                highlighted = [self.highlighted]
            )
        )

        s_data = source_true.data
        s_data_string = source_true_string.data

        source_string = ColumnDataSource(
            data =dict(
                degree=data_string[0],
                count=data_string[1],
                pagerank=data_string[2],
                pagerank_count=data_string[3],
                clustering_coefficient=data_string[4],
                clustering_coefficient_count=data_string[5],
                v1=s_data_string['v1'],
                v2=s_data_string['v2'],
                v3=s_data_string['v3'],
                v4=s_data_string['v4'],
                v5=s_data_string['v5'],
                v6=s_data_string['v6'],
                v7=s_data_string['v7'],
                v8=s_data_string['v8']
            )
        )

        self.source = ColumnDataSource(
            data =dict(
                degree=data[0],
                count=data[1],
                pagerank=data[2],
                pagerank_count=data[3],
                clustering_coefficient=data[4],
                clustering_coefficient_count=data[5],
                v1=s_data['v1'],
                v2=s_data['v2'],
                v3=s_data['v3'],
                v4=s_data['v4'],
                v5=s_data['v5'],
                v6=s_data['v6'],
                v7=s_data['v7'],
                v8=s_data['v8']
            )
        )

        highlightedsource_true = ColumnDataSource(
            data =dict(
                v1=data.iloc[self.highlightedNodeIDs][6],
                v2=data.iloc[self.highlightedNodeIDs][7],
                v3=data.iloc[self.highlightedNodeIDs][8],
                v4=data.iloc[self.highlightedNodeIDs][9],
                v5=data.iloc[self.highlightedNodeIDs][10],
                v6=data.iloc[self.highlightedNodeIDs][11],
                v7=data.iloc[self.highlightedNodeIDs][12],
                v8=data.iloc[self.highlightedNodeIDs][13],
                v9=data.iloc[self.highlightedNodeIDs][14],
                v10=data.iloc[self.highlightedNodeIDs][15]
            )
        )
        highlighted_s_data = highlightedsource_true.data

        self.highlightSource = ColumnDataSource(
            data = dict(
                degree=data.iloc[self.highlightedNodeIDs][0],
                count=data.iloc[self.highlightedNodeIDs][1],
                pagerank=data.iloc[self.highlightedNodeIDs][2],
                pagerank_count=data.iloc[self.highlightedNodeIDs][3],
                clustering_coefficient=data.iloc[self.highlightedNodeIDs][4],
                clustering_coefficient_count=data.iloc[self.highlightedNodeIDs][5],
                v1=highlighted_s_data['v1'],
                v2=highlighted_s_data['v2'],
                v3=highlighted_s_data['v3'],
                v4=highlighted_s_data['v4'],
                v5=highlighted_s_data['v5'],
                v6=highlighted_s_data['v6'],
                v7=highlighted_s_data['v7'],
                v8=highlighted_s_data['v8']
            )
        )

        degree_x_p1 = DataRange1d("degree")
        degree_x_p2 = DataRange1d("degree")
        count_y = DataRange1d("count")
        pagerank_y = DataRange1d("pagerank")
        pagerank_x = DataRange1d("pagerank")
        pagerank_count = DataRange1d("pagerank_count")
        clustering_coefficient = DataRange1d("clustering_coefficient")
        clustering_coefficient_count = DataRange1d("clustering_coefficient_count")

        p4_x = DataRange1d("v1")
        p4_y = DataRange1d("v2")
        p5_x = DataRange1d("v3")
        p5_y = DataRange1d("v4")
        p6_x = DataRange1d("v5")
        p6_y = DataRange1d("v6")
        p7_x = DataRange1d("v7")
        p7_y = DataRange1d("v8")

        # v4 = DataRange1d("v4")
        # v5 = DataRange1d("v5")
        # v6 = DataRange1d("v6")
        # v7 = DataRange1d("v7")
        # v8 = DataRange1d("v8")
        # v9 = DataRange1d("v9")

        window_size = 350
        between_window_size = 40
        border_size = 6

        def make_plot(xname, yname, isLog, needsColor, xcolor, needsS, xdr, ydr, xax=False, yax=False):
            mbl = between_window_size if yax else 0
            mbb = between_window_size if xax else 0

            # TODO: Currently there isn't any support by Bokeh to limit the number of hover tooltips apearing
            # which crashes the webpage if too many points are on top of each other at the same time
            # hover = HoverTool(tooltips=[
            #     (xname, "$x"),
            #     (yname, "$y")
            # ])

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
            
            if not needsS:
                plot.xaxis.axis_label = xname
                plot.yaxis.axis_label = yname
            else:
                plot.xaxis.axis_label = "s" + xname
                plot.yaxis.axis_label = "s" + yname
            

            if self.highlighted:
                    circle = Circle(x=xname, y=yname, fill_color = "grey", fill_alpha=0.6, size=5, line_color=None)
                    highlightCircle = Circle(x=xname, y=yname, fill_color = "red", fill_alpha=0.6, size=10, line_color=None)
                    r = plot.add_glyph(self.source, circle)
                    r.nonselection_glyph = Circle(fill_color="grey", fill_alpha = 0.1, line_color=None)
                    xdr.renderers.append(r)
                    ydr.renderers.append(r)

                    hr = plot.add_glyph(self.highlightSource, highlightCircle)
                    hr.nonselection_glyph = Circle(fill_color="grey", fill_alpha = 0.1, line_color=None)
                    xdr.renderers.append(hr)
                    ydr.renderers.append(hr)
            else:
                if needsColor:
                    circle = Circle(x=xname, y=yname, fill_color={'field': xcolor, 'transform': color_mapper}, fill_alpha=0.6, size=5, line_color=None)
                else:
                    circle = Circle(x=xname, y=yname, fill_color = "blue", fill_alpha=0.6, size=5, line_color=None)
                r = plot.add_glyph(self.source, circle)
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


        plots_row1 = []
        row = []

        plot1 = make_plot("degree", "count", True, False, "", False, degree_x_p1, count_y)
        plot2 = make_plot("degree", "pagerank", True, True, "pagerank_count", False, degree_x_p2, pagerank_y)
        plot3 = make_plot("pagerank", "pagerank_count", True, False, "", False, pagerank_x, pagerank_count)
        plot4 = make_plot("clustering_coefficient", "clustering_coefficient_count", True, False, "", False, clustering_coefficient, clustering_coefficient_count)

        row.append(plot1)
        row.append(plot2)
        row.append(plot3)
        row.append(plot4)
        plots_row1.append(row)

        plots_row2 = []
        row = []

        plot5 = make_plot("v1", "v2", False, False, "", True, p4_x, p4_y)
        plot6 = make_plot("v3", "v4", False, False, "", True, p5_x, p5_y)
        plot7 = make_plot("v5", "v6", False, False, "", True, p6_x, p6_y)
        plot8 = make_plot("v7", "v8", False, False, "", True, p7_x, p7_y)

        row.append(plot5)
        row.append(plot6)
        row.append(plot7)
        row.append(plot8)
        plots_row2.append(row)

        stats = Div(text='', width=9000)

        # Tickers
        ticker1x = Select(title="x1-axis:", value="sv1", options=["sv1", "sv2", "sv3", "sv4", "sv5", "sv6", "sv7", "sv8", "sv9", "sv10"])
        ticker1y = Select(title="y1-axis:", value="sv2", options=["sv1", "sv2", "sv3", "sv4", "sv5", "sv6", "sv7", "sv8", "sv9", "sv10"])
        ticker2x = Select(title="x2-axis:", value="sv3", options=["sv1", "sv2", "sv3", "sv4", "sv5", "sv6", "sv7", "sv8", "sv9", "sv10"])
        ticker2y = Select(title="y2-axis:", value="sv4", options=["sv1", "sv2", "sv3", "sv4", "sv5", "sv6", "sv7", "sv8", "sv9", "sv10"])
        ticker3x = Select(title="x3-axis:", value="sv5", options=["sv1", "sv2", "sv3", "sv4", "sv5", "sv6", "sv7", "sv8", "sv9", "sv10"])
        ticker3y = Select(title="y3-axis:", value="sv6", options=["sv1", "sv2", "sv3", "sv4", "sv5", "sv6", "sv7", "sv8", "sv9", "sv10"])
        ticker4x = Select(title="x4-axis:", value="sv7", options=["sv1", "sv2", "sv3", "sv4", "sv5", "sv6", "sv7", "sv8", "sv9", "sv10"])
        ticker4y = Select(title="y4-axis:", value="sv8", options=["sv1", "sv2", "sv3", "sv4", "sv5", "sv6", "sv7", "sv8", "sv9", "sv10"])

        tickers_rowx = bokeh.layouts.row(ticker1x, ticker2x, ticker3x, ticker4x)
        tickers_rowy = bokeh.layouts.row(ticker1y, ticker2y, ticker3y, ticker4y)

        plots_row1 = gridplot(plots_row1)
        plots_row2 = gridplot(plots_row2)

        # plots_row = gridplot([[plot1, plot2, plot3],[plot4, plot5, plot6]])

        layout = bokeh.layouts.column(plots_row1, tickers_rowx, tickers_rowy, plots_row2, stats, sizing_mode='scale_width')

        callback_ticker1x = CustomJS(args=dict(source=self.source, source_true=source_true, plot=plot5), code="""
            console.log("Callback_ticker1x is called");
            var value = cb_obj.get("value");
            value = value.substring(1);
            source['data']['v1'] = source_true['data'][value];
            plot.below[0].axis_label = "s"+value;
            source.trigger('change')
        """)

        callback_ticker1y = CustomJS(args=dict(source=self.source, source_true=source_true, plot=plot5), code="""
            console.log("Callback_ticker1y is called");
            var value = cb_obj.get("value");
            value = value.substring(1);
            source['data']['v2'] = source_true['data'][value];
            plot.left[0].axis_label = "s"+value;
            source.trigger('change')
        """)

        callback_ticker2x = CustomJS(args=dict(source=self.source, source_true=source_true,plot=plot6), code="""
            console.log("Callback_ticker2x is called");
            var value = cb_obj.get("value");
            value = value.substring(1);
            source['data']['v3'] = source_true['data'][value];
            plot.below[0].axis_label = "s"+value;
            source.trigger('change')
        """)

        callback_ticker2y = CustomJS(args=dict(source=self.source, source_true=source_true,plot=plot6), code="""
            console.log("Callback_ticker2y is called");
            var value = cb_obj.get("value");
            value = value.substring(1);
            source['data']['v4'] = source_true['data'][value];
            plot.left[0].axis_label = "s"+value;
            source.trigger('change')
        """)

        callback_ticker3x = CustomJS(args=dict(source=self.source, source_true=source_true, plot=plot7), code="""
            console.log("Callback_ticker3x is called");
            var value = cb_obj.get("value");
            value = value.substring(1);
            source['data']['v5'] = source_true['data'][value];
            plot.below[0].axis_label = "s"+value;
            source.trigger('change')
        """)

        callback_ticker3y = CustomJS(args=dict(source=self.source, source_true=source_true, plot=plot7), code="""
            console.log("Callback_ticker3y is called");
            var value = cb_obj.get("value");
            value = value.substring(1);
            source['data']['v6'] = source_true['data'][value];
            plot.left[0].axis_label = "s"+value;
            source.trigger('change')
        """)

        callback_ticker4x = CustomJS(args=dict(source=self.source, source_true=source_true, plot=plot8), code="""
            console.log("Callback_ticker4x is called");
            var value = cb_obj.get("value");
            value = value.substring(1);
            source['data']['v7'] = source_true['data'][value];
            plot.below[0].axis_label = "s"+value;
            source.trigger('change')
        """)

        callback_ticker4y = CustomJS(args=dict(source=self.source, source_true=source_true, plot=plot8), code="""
            console.log("Callback_ticker4y is called");
            var value = cb_obj.get("value");
            value = value.substring(1);
            source['data']['v8'] = source_true['data'][value];
            plot.left[0].axis_label = "s"+value;
            source.trigger('change')
        """)

        callback = CustomJS(args=dict(source=self.source, source_true=source_true, source_new=source_state, stats=stats,
            source_string=source_string, source_true_string=source_true_string,
            tk1x=ticker1x, tk1y=ticker1y, tk2x=ticker2x, tk2y=ticker2y, tk3x=ticker3x, tk3y=ticker3y, tk4x=ticker4x, tk4y=ticker4y), code="""
            console.log("Selected callback was called");
            var inds = cb_obj.selected['1d'].indices;
            console.log(inds);

            if (inds.length > 0) {        
                state = Number(source_new['data']['state'][0])
                console.log("State is:", state)

                var name = ['degree', 'count', 'degree', 'pagerank', 'pagerank', 'pagerank_count', 'clustering_coefficient', 'clustering_coefficient_count', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8'];
                var real_name = ['degree', 'count', 'degree', 'pagerank_t', 'pagerank_t', 'pagerank_t_count', 'clustering_coefficient_t', 'clustering_coefficient_t_count', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8'];

                // Update the right names for the eigenvectors
                if (state >= 5 && state <= 8) {
                    if (state === 5) {
                        name8 = tk1x.get("value");
                        name9 = tk1y.get("value");
                        name8 = name8.substring(1);
                        name9 = name9.substring(1);
                        name[8] = name8;
                        name[9] = name9;
                        real_name[8] = name8;
                        real_name[9] = name9;
                    }
                    else if (state === 6) {
                        name10 = tk2x.get("value");
                        name11 = tk2y.get("value");
                        name10 = name10.substring(1);
                        name11 = name11.substring(1);
                        name[10] = name10;
                        name[11] = name11;
                        real_name[10] = name10;
                        real_name[11] = name11;
                    }
                    else if (state === 7) {
                        name12 = tk3x.get("value");
                        name13 = tk3y.get("value");
                        name12 = name12.substring(1);
                        name13 = name13.substring(1);
                        name[12] = name12;
                        name[13] = name13;
                        real_name[12] = name12;
                        real_name[13] = name13;
                    }
                    else if (state === 8) {
                        name14 = tk4x.get("value");
                        name15 = tk4y.get("value");
                        name14 = name14.substring(1);
                        name15 = name15.substring(1);
                        name[14] = name14;
                        name[15] = name15;
                        real_name[14] = name14;
                        real_name[15] = name15;
                    }
                }

                // console.log(name);
                // console.log(real_name);

                if (state <= 4) {
                    var x1 = source_string['data'][name[2*state-2]][inds[0]];
                    var y1 = source_string['data'][name[2*state-1]][inds[0]];
                }
                else {
                    var x1 = source_true_string['data'][name[2*state-2]][inds[0]];
                    var y1 = source_true_string['data'][name[2*state-1]][inds[0]];
                }
                
                var x1_name = real_name[2*state-2];
                var y1_name = real_name[2*state-1];

                // Adjusting for real names
                if (state >= 5 && state <= 8) {
                    val_x1 = x1_name[1];
                    val_y1 = y1_name[1];

                    if (x1_name === "v10") {
                        x1_name = x1_name[0] + "_10_t";
                    }
                    else {
                        x1_name = x1_name[0] + "_" + val_x1 + "_t";
                    }
                    
                    if (y1_name === "v10") {
                        y1_name = y1_name[0] + "_10_t";
                    }
                    else {
                        y1_name = y1_name[0] + "_" + val_y1 + "_t"
                    }
                }

                // console.log("Inside Callback:",x1,y1,x1_name,y1_name);
                nodeSelected(x1, y1, x1_name, y1_name);
            }
        """)

        event_callback_1 = CustomJS(args=dict(source=source_state),code="""
            source['data']['state'] = [1];
            h = source['data']['highlighted'][0];
            if (h === true) {
                console.log("Changing Highlighted Value");
                source['data']['highlighted'] = [false];
                disableHighlighting();
            }
            console.log(1111111)
        """)
        event_callback_2 = CustomJS(args=dict(source=source_state),code="""
            source['data']['state'] = [2];
            h = source['data']['highlighted'][0];
            if (h === true) {
                console.log("Changing Highlighted Value");
                source['data']['highlighted'] = [false];
                disableHighlighting();
            }
            console.log(2222222)
        """)
        event_callback_3 = CustomJS(args=dict(source=source_state),code="""
            source['data']['state'] = [3];
            h = source['data']['highlighted'][0];
            if (h === true) {
                console.log("Changing Highlighted Value");
                source['data']['highlighted'] = [false];
                disableHighlighting();
            }
            console.log(3333333)
        """)
        event_callback_4 = CustomJS(args=dict(source=source_state),code="""
            source['data']['state'] = [4];
            h = source['data']['highlighted'][0];
            if (h === true) {
                console.log("Changing Highlighted Value");
                source['data']['highlighted'] = [false];
                disableHighlighting();
            }
            console.log(4444444)
        """)
        event_callback_5 = CustomJS(args=dict(source=source_state),code="""
            source['data']['state'] = [5];
            h = source['data']['highlighted'][0];
            if (h === true) {
                console.log("Changing Highlighted Value");
                source['data']['highlighted'] = [false];
                disableHighlighting();
            }
            console.log(5555555)
        """)
        event_callback_6 = CustomJS(args=dict(source=source_state),code="""
            source['data']['state'] = [6];
            h = source['data']['highlighted'][0];
            if (h === true) {
                console.log("Changing Highlighted Value");
                source['data']['highlighted'] = [false];
                disableHighlighting();
            }
            console.log(6666666)
        """)
        event_callback_7 = CustomJS(args=dict(source=source_state),code="""
            source['data']['state'] = [7];
            h = source['data']['highlighted'][0];
            if (h === true) {
                console.log("Changing Highlighted Value");
                source['data']['highlighted'] = [false];
                disableHighlighting();
            }
            console.log(7777777)
        """)
        event_callback_8 = CustomJS(args=dict(source=source_state),code="""
            source['data']['state'] = [8];
            h = source['data']['highlighted'][0];
            if (h === true) {
                console.log("Changing Highlighted Value");
                source['data']['highlighted'] = [false];
                disableHighlighting();
            }
            console.log(88888888)
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
        plot7.js_on_event(Tap, event_callback_7)
        plot7.js_on_event(Press, event_callback_7)
        plot8.js_on_event(Tap, event_callback_8)
        plot8.js_on_event(Press, event_callback_8)

        self.source.js_on_change("selected", callback)

        ticker1x.js_on_change('value', callback_ticker1x)
        ticker1y.js_on_change('value', callback_ticker1y)
        ticker2x.js_on_change('value', callback_ticker2x)
        ticker2y.js_on_change('value', callback_ticker2y)
        ticker3x.js_on_change('value', callback_ticker3x)
        ticker3y.js_on_change('value', callback_ticker3y)
        ticker4x.js_on_change('value', callback_ticker4x)
        ticker4y.js_on_change('value', callback_ticker4y)
    
        script, div = components(layout, CDN)

        return {
            "graph_script": script, 
            "graph": div
        }
    
    # TODO change selected nodes
    def change_selected_nodes(self, selected_ids):
        testcall = CustomJS(args=dict(source=self.source), code="""
            console.log("Selected callback was called");
            var inds = cb_obj.selected['1d'].indices;
            console.log(inds);
        """)
        print "change_selected_nodes"
        print self.source.selected['1d']
        self.source.selected['1d']['indices'] = selected_ids
        print self.source.selected['1d']
        self.source.js_on_change("selected", testcall)
