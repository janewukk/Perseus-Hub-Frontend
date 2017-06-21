from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import ConnectionDoesNotExist  
from django.db.models import F
from django.db.models import Q

import app
from app.models import *

import os
import time
import string
import random
import json

import pandas as pd
import sys

from decimal import *
from app.services.graph import *
from app.controllers.dashboard import *
from django.template.loader import render_to_string

def ClickPlot(request):
    val = "hi from ClickPlot"
    data = json.loads(request.body)
    x = data['x1']
    y = data['y1']
    x_name = data['x_name']
    y_name = data['y_name']
    print(x_name)
    print(y_name)
    print(x)
    print(y)

    # Check if we have count vs degree, or pagerank_count vs pagerank 
    if (x_name == "degree" and y_name == "count"):
        results = Node.objects.filter(degree = x)[:10]
    elif (x_name == "pagerank_t" and y_name == "pagerank_t_count"):
        print "pagerank_t vs. pagerank_t_count"
        results = Node.objects.raw("Select * from app_node where " + x_name + " = " + x + " LIMIT 10;")
        # results = Node.objects.filter(pagerank_t = x)[:10]
    else:
        print 'here'
        results = Node.objects.raw("Select * from app_node where " + x_name + " = " + x + " and " + y_name + " = " + y + " LIMIT 10;")
        # results = Node.objects.filter(pagerank_t = y)[:10]
        # results = Node.objects.filter(**{x_name: x, y_name: y})[:10]
    
    output = []

    print results

    for result in results:
        item = []
        item.append(result.nodeid)
        item.append(result.degree)
        item.append(result.pagerank)
        item.append(result.v_1)
        output.append(item)

    json_data = json.dumps(output)

    return HttpResponse(json_data)

previousNodeID = 0
storedNodes =  []

def GetEgonet(request):
    global previousNodeID
    global storedNodes

    resultStr = ''
    
    data = json.loads(request.body)
    nodeid = data['id']
    print "Generating egonet for node " + str(nodeid)

    outedges = Edge.objects.filter(fromNode = nodeid)
    inedges = Edge.objects.filter(toNode = nodeid)
    nodes = set()
    nodes_ego = set()

    for oe in outedges:
        nodes.add(oe.toNode)

    for ie in inedges:
        nodes.add(ie.fromNode)

    nodes.add(nodeid)

    sampleNum = 10
    
    if previousNodeID != nodeid:
        pagerankDict = dict()
        for curNode in nodes:
            curNode_pagerankList = Node.objects.filter(nodeid = curNode)
            for temp in curNode_pagerankList:
                curNode_pagerank = float(temp.pagerank)
            pagerankDict.update({curNode: curNode_pagerank})
        
        pagerankDict_Sorted = sorted(pagerankDict.items(), key=lambda d:d[1], reverse = True)
        
        pagerankDict_Sorted_List = []
        for temp in pagerankDict_Sorted:
            pagerankDict_Sorted_List.append(temp[0])
        
        storedNodes = pagerankDict_Sorted_List          
    else:
        pagerankDict_Sorted_List = storedNodes[sampleNum:]
        storedNodes = storedNodes[sampleNum:]

    # sample the neighbor for egonet
    if len(pagerankDict_Sorted_List) > sampleNum:
        #nodes = random.sample(nodes,sampleNum)
        nodes_ego = pagerankDict_Sorted_List[:sampleNum]
        nodes_ego.append(nodeid)
    else:
        nodes_ego = pagerankDict_Sorted_List

    validEdges_selected = Edge.objects.filter(fromNode__in=nodes_ego, toNode__in=nodes_ego)

    dictionary = {}
    dictionary['Nodes'] = []
    dictionary['Links'] = []

    for n in nodes_ego:
        temp_dic = {"Id": str(n)}
        dictionary['Nodes'].append(temp_dic)

    for e in validEdges_selected:
        temp_dic = {"Source": str(e.fromNode), "Target": str(e.toNode), "Value": str(e.weight)}
        dictionary['Links'].append(temp_dic)
        # resultStr = resultStr + str(e.fromNode) + "\t" + str(e.toNode)+ "\t" + str(e.weight) + "\n"

    json_data = json.dumps(dictionary)

    return HttpResponse(json_data, content_type="application/json")

def GetAdjMatrix(request):
	data = json.loads(request.body)
	nodeid = data['nodeid']
	print(nodeid)
	## begin di's code
	adjNumMax = 100
	resultStr = ""
	nodes = set()
	outedges = Edge.objects.filter(fromNode = nodeid)
	inedges = Edge.objects.filter(toNode = nodeid)
	
	for oe in outedges:
		nodes.add(oe.toNode)
	for ie in inedges:
		nodes.add(ie.fromNode)
	nodes.add(nodeid)
	print("here 1111")

	pagerankDict = dict()
	for curNode in nodes:
		curNode_pagerankList = Node.objects.filter(nodeid = curNode)
		for temp in curNode_pagerankList:
			curNode_pagerank = float(temp.pagerank) #temp.pagerank
		pagerankDict.update({curNode: curNode_pagerank})
	print("here 22222")
		
	pagerankDict_Sorted = sorted(pagerankDict.items(), key=lambda d:d[1], reverse = True)
		
	pagerankDict_Sorted_List = []
	for temp in pagerankDict_Sorted:
		pagerankDict_Sorted_List.append(temp[0])
		
	pagerankDict_Sorted_List
	print("here 33333")


	if len(pagerankDict_Sorted_List) > adjNumMax:
		nodes_adj = pagerankDict_Sorted_List[:adjNumMax]
	else:
		nodes_adj = pagerankDict_Sorted_List
	print("here 33333")

	print(nodes_adj)


	validEdges = Edge.objects.filter(fromNode__in=nodes_adj, toNode__in=nodes_adj)
	print ("writing starts")

	response_data = {}
	response_data['edges'] = ''
	response_data['nodes_src'] = ''
	response_data['nodes_dst'] = ''
	print("here 33333")

	source = []
	target = []
	nodes_unique = set()
	nodes_unique.add(nodeid)


	for ele in validEdges:
		response_data['edges'] = response_data['edges'] + str(ele.fromNode) + "\t" + str(ele.toNode)+ ";"
		source.append(ele.fromNode)
		target.append(ele.toNode)
		nodes_unique.add(ele.fromNode)
		nodes_unique.add(ele.toNode)

	nodes = []
	for ele in nodes_unique:
		nodes.append(ele)

	response_data = {
		'source': source,
		'target': target,
		'nodes': nodes
	}

	print(json.dumps(response_data))

	return HttpResponse(json.dumps(response_data), content_type="application/json")

def GetABOD(request):
    file = "data/combined_scores_ABOD.csv"
    data = pd.read_csv(file, skipinitialspace=True, escapechar="\\", header=None)

    # Sort the data to get the top 10 anomaly scores
    data = data.sort_values([0], ascending=[False])
    nodes = data[0][0:10].index.tolist()
    scores = data[0][0:10].tolist()

    # Read aggregate data file in order to find which aggregate nodes correspond to the top 10 anomalous nodes
    aggfile = "data/combined_data.csv"
    fullfile = "data/full_data.csv"
    aggdata = pd.read_csv(aggfile, skipinitialspace=True, escapechar="\\", header=None)
    fulldata = pd.read_csv(fullfile, skipinitialspace=True, escapechar="\\", header=None)

    # Perform filtering to find the relevant aggregate node ids
    aggregate_node_ids = []
    for row in nodes:
        val = fulldata.loc[[row]]
        # print val
        degree = val[1].values[0]
        count = val[2].values[0]
        pagerank_t = val[4].values[0]
        clustering_coef_t = val[7].values[0]
        rel_points = aggdata.loc[(aggdata[0] == degree) & (aggdata[1] == count) & (aggdata[2] == pagerank_t) & (aggdata[4] == clustering_coef_t)]
        aggregate_node_ids.append(rel_points.index.tolist()[0])


    # TODO Update the bokeh plot so that only the top 10 anomalous points are selected
    # Make all the nodes in the aggregate_node_ids selected and the rest unselected in the bokeh visualization

    # Perform a reload of the template similar to DatasetViewController
    # graph.change_selected_nodes(aggregate_node_ids)

    # dataset = None
    # graph_data = graph.graph_from_file('combined_data.csv')

    # html = render_to_string('dashboard/dataset-template.html', {
	# 			'dataset' : dataset,
	# 			'graph_script' : graph_data['graph_script'],
	# 			'graph' : graph_data['graph']})

    # return HttpResponse(html)
    # return render(request, 'dashboard/dataset-template.html',

    response_data = {
		'nodeid': nodes,
		'score': scores,
        'aggnodeid': aggregate_node_ids
    }

    print(json.dumps(response_data))
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def GetGFADD(request):
    file = "data/combined_scores_GFADD.csv"
    data = pd.read_csv(file, skipinitialspace=True, escapechar="\\", header=None)

    # Sort the data to get the top 10 anomaly scores
    data = data.sort_values([0], ascending=[False])

    nodes = data[0][0:10].index.tolist()
    scores = data[0][0:10].tolist()


    # Read aggregate data file in order to find which aggregate nodes correspond to the top 10 anomalous nodes
    aggfile = "data/combined_data.csv"
    fullfile = "data/full_data.csv"
    aggdata = pd.read_csv(aggfile, skipinitialspace=True, escapechar="\\", header=None)
    fulldata = pd.read_csv(fullfile, skipinitialspace=True, escapechar="\\", header=None)

    # Perform filtering to find the relevant aggregate node ids
    aggregate_node_ids = []
    for row in nodes:
        val = fulldata.loc[[row]]
        # print val
        degree = val[1].values[0]
        count = val[2].values[0]
        pagerank_t = val[4].values[0]
        clustering_coef_t = val[7].values[0]
        rel_points = aggdata.loc[(aggdata[0] == degree) & (aggdata[1] == count) & (aggdata[2] == pagerank_t) & (aggdata[4] == clustering_coef_t)]
        aggregate_node_ids.append(rel_points.index.tolist()[0])


    # TODO Update the bokeh plot so that only the top 10 anomalous points are selected
    # Make all the nodes in the aggregate_node_ids selected and the rest unselected in the bokeh visualization

    # Perform a reload of the template similar to DatasetViewController
    # graph.change_selected_nodes(aggregate_node_ids)

    # dataset = None
    # graph_data = graph.graph_from_file('combined_data.csv')

    # html = render_to_string('dashboard/dataset-template.html', {
	# 			'dataset' : dataset,
	# 			'graph_script' : graph_data['graph_script'],
	# 			'graph' : graph_data['graph']})

    # return HttpResponse(html)
    # return render(request, 'dashboard/dataset-template.html',

    response_data = {
		'nodeid': nodes,
		'score': scores,
        'aggnodeid': aggregate_node_ids
    }

    print(json.dumps(response_data))

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def GetCombAnScore(request):
    file = "data/combined_scores.csv"
    data = pd.read_csv(file, skipinitialspace=True, escapechar="\\", header=None)

    # Sort the data to get the top 10 anomaly scores
    data = data.sort_values([0], ascending=[False])
    nodes = data[0][0:10].index.tolist()
    scores = data[0][0:10].tolist()

    # Read aggregate data file in order to find which aggregate nodes correspond to the top 10 anomalous nodes
    aggfile = "data/combined_data.csv"
    fullfile = "data/full_data.csv"
    aggdata = pd.read_csv(aggfile, skipinitialspace=True, escapechar="\\", header=None)
    fulldata = pd.read_csv(fullfile, skipinitialspace=True, escapechar="\\", header=None)

    # Perform filtering to find the relevant aggregate node ids
    aggregate_node_ids = []
    for row in nodes:
        val = fulldata.loc[[row]]
        # print val
        degree = val[1].values[0]
        count = val[2].values[0]
        pagerank_t = val[4].values[0]
        clustering_coef_t = val[7].values[0]
        rel_points = aggdata.loc[(aggdata[0] == degree) & (aggdata[1] == count) & (aggdata[2] == pagerank_t) & (aggdata[4] == clustering_coef_t)]
        aggregate_node_ids.append(rel_points.index.tolist()[0])


    # TODO Update the bokeh plot so that only the top 10 anomalous points are selected
    # Make all the nodes in the aggregate_node_ids selected and the rest unselected in the bokeh visualization

    # Perform a reload of the template similar to DatasetViewController
    # graph.change_selected_nodes(aggregate_node_ids)

    # dataset = None
    # graph_data = graph.graph_from_file('combined_data.csv')

    # html = render_to_string('dashboard/dataset-template.html', {
	# 			'dataset' : dataset,
	# 			'graph_script' : graph_data['graph_script'],
	# 			'graph' : graph_data['graph']})

    # return HttpResponse(html)
    # return render(request, 'dashboard/dataset-template.html',

    response_data = {
		'nodeid': nodes,
		'score': scores,
        'aggnodeid': aggregate_node_ids
    }

    print(json.dumps(response_data))
    return HttpResponse(json.dumps(response_data), content_type="application/json")