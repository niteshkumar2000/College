import pandas as pd
import numpy as np
import math
import networkx as nx
# from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt

def reversal_node(df_row, current_node):
    if df_row['to'] == current_node:
        df_row['from'], df_row['to'] = df_row['to'],df_row['from']
    return df_row

def get_all_edges(closed, parent, end_node, edges_list):
    edges = []
    for index, row in closed.iterrows():
        edge_ = edges_list.loc[((edges_list['from']==row['node'])&(edges_list['to']==parent[row['node']]))|((edges_list['from']==parent[row['node']])&(edges_list['to']==row['node']))]
        if not edge_.empty:
            edges.append((parent[row['node']], row['node'], edge_.iloc[0]['weights']))
    weight_goal = edges_list.loc[(edges_list['from']==parent[end_node])&(edges_list['to']==end_node)]
    edges.append((parent[end_node], end_node,weight_goal.iloc[0]['weights']))
    return edges

def print_graph(path):
    G = nx.Graph()
    G.add_weighted_edges_from(path)
    pos = graphviz_layout(G, prog="dot")
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

def get_path_to_goal(parent, end_node):
    current_node = end_node
    path_to_goal = []
    while current_node != 'Parent':
        path_to_goal.append((parent[current_node], current_node))
        current_node = parent['current_node']
    return path_to_goal[:-1]

def hillClimbing(edges, straight_dist, start_node, end_node):
    open_structure = pd.DataFrame([[start_node, straight_dist[start_node]]], columns=['node', 'estimated_cost'])
    closed_structure = pd.DataFrame(columns=['node','estimated_cost'])
    success = False
    parent = { start_node: 'Parent'}
    cost_from_parent = { start_node: 0 }
    previous_cost = math.inf
    while not open_structure.empty:
        current_node_data = open_structure.iloc[0]
        current_node, estimated_cost = current_node_data['node'], current_node_data['estimated_cost']
        open_structure = open_structure.iloc[1:]
        if estimated_cost < previous_cost:
            if end_node == current_node:
                success = True
                break
            closed_structure = closed_structure.append(current_node_data)
            closed_structure = closed_structure.reset_index(drop=True)
            next_edges = edges.loc[(edges['from'] == current_node)|(edges['to'] == current_node)]
            next_edges = next_edges.apply(lambda row: reversal_node(row, current_node), axis=1)
            for index, row  in next_edges.iterrows():
                open_node = open_structure.loc[(open_structure['node']==row['to'])]
                if open_node.empty:
                    open_structure = open_structure.append(pd.DataFrame([[row['to'], straight_dist[row['to']]]], columns=['node', 'estimated_cost']))
                    parent[row['to']] = row['from']
                    cost_from_parent[row['to']] = cost_from_parent[row['from']] + row['weights']
            open_structure = open_structure.sort_values(by=['estimated_cost']).reset_index(drop=True)
            previous_cost = estimated_cost
        else:
            success = False
            break
    return { "success": success , "expanded_node": closed_structure, "current_open": open_structure, "current_node": current_node, "parent": parent}

edges = pd.read_csv('edge_list.csv')
straight_dist = pd.read_csv('straight_line.csv', header=None, index_col=0, squeeze=True).to_dict()
start_node, end_node = 'A','R'
result = hillClimbing(edges, straight_dist, start_node, end_node)
print("========================")
print(" Success: {}".format(result['success']))
print("======TRAVERSED========")
print(result['expanded_node'])
print("=======OPEN=========")
print(result['current_open'])
if result['success']:
    path = get_all_edges(result['expanded_node'], result['parent'], end_node, edges)
    print(path)
    # print_graph(path)
