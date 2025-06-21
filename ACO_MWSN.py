from __future__ import division
import constants
import random

def get_path(nest,food_source,graph):### 1 based indexing
    ### graph is a 2d matrix containing distance between node(i) and node(j) in cell value graph[i][j]
    ### return optimal(or suboptimal) path(as python_list) for travel between source and food_source
    
    pheromone_graph = [ [ 0 for i in range(constants.MOBILE_NODE_COUNT+1)] for j in range(constants.MOBILE_NODE_COUNT+1)]
    ### initialize pheromone_graph
    for i in range(1,len(graph)):
        for j in range(1,len(graph)):
            if graph[i][j]!=-1:    
                pheromone_graph[i][j]=constants.INITIAL_PHEROMONE
                
    for i in range(constants.ANTS_PER_ITERATION):
        path, details, pheromone_graph = ants_forward_mode(nest, food_source, pheromone_graph, graph)
        
        ### details is list of tuples, tuple = (LQI,Delay link)
        path = eliminate_loops(path,constants.MOBILE_NODE_COUNT)
        
        ### path cost not calculated, unlike S-ACO
        
        pheromone_graph = ants_backward_mode(nest, food_source, pheromone_graph, path, graph, details)#path_cost)
    
    return path

def PRR():### packet reception rate
    return random.random()*constants.PACKET_RECEPTION_RATE

def normalied_RSSI_mean():### received signal strength indicator
    RSSI_mean = (random.random()*60)-100
    return (RSSI_mean+100)/60

def get_LQI(node_i, node_j, dist, existing_pheromone):
    return PRR()*normalied_RSSI_mean()
    #return random.random()

def get_Dlink(node_i, node_j, dist):
    d_prop = dist/constants.SIGNAL_PROPAGATION_SPEED
    d_proc = constants.PROCESSING_DELAY
    return d_prop + d_proc
    #return 1

def FA_pheromone(LQI):
    one_to_one_point_five = 1 + random.random()/2
    return LQI * one_to_one_point_five
    #return 1

def ants_forward_mode(nest, food_source, pheromone_graph, graph):
    previous_node = -1
    curr_node = nest
    path = [curr_node]
    details = []
    steps = 0
    while curr_node!=food_source and steps <= constants.ANTS_NUMBER_STEPS:
        LQI = -1
        next_node = previous_node
        for node_j in range(1,len(pheromone_graph)):
            if node_j!=previous_node and node_j!=curr_node and pheromone_graph[curr_node][node_j]!=0:
                curr_link_LQI = get_LQI(curr_node, node_j, graph[curr_node][node_j], pheromone_graph[curr_node][node_j])
                if LQI < curr_link_LQI:
                    LQI = curr_link_LQI
                    next_node = node_j
                    
        ### updating pheromone graph
        pheromone_graph[curr_node][next_node] += FA_pheromone(LQI)
        
        details += [(LQI,get_Dlink(curr_node, next_node, graph[curr_node][next_node]))]
        path += [next_node]
        
        previous_node=curr_node
        curr_node = next_node
        steps += 1
    return (path,details,pheromone_graph)
    
def eliminate_loops(path, n):### n = number of nodes
    ### eliminates loops in same order as they were created
    ### 1 based indexing
    visited = [ 0 for i in range(n+1)]
    for i in range(len(path)):
        if visited[path[i]]==0:
            visited[path[i]]=1
        else:
            j=i-1
            while path[j]!=path[i]:
                j-=1
            while j<i:
                if path[i]!=-1:
                    visited[path[j]]=0
                path[j]=-1
                j+=1
            visited[path[i]]=1
    loop_free_path = []
    for i in path:
        if i!=-1:
            loop_free_path += [i]
    return loop_free_path

def ants_backward_mode(nest, source_food, pheromone_graph, path, graph, details):
    ### Assuming ACO_MWSN doesn't take in account evaporation
    ### pheromone_graph = evaporate_pheromone(pheromone_graph,constants.PHEROMONE_EVAPORATION_RATE)
    for i in range(len(path)-1,0,-1):
        node_j = path[i]
        node_i = path[i-1]  ## node_i -> node_j | travelled by ant in forward direction
        LQI, D_link = details[i-1]
        pheromone_graph[node_i][node_j] += LQI - D_link
        ### pheromone_graph[node_i][node_j] += 1/path_cost
        pheromone_graph[node_j][node_i] = pheromone_graph[node_i][node_j]
    return pheromone_graph

def evaporate_pheromone(pheromone_graph,evaporation_parameter):
    ### ant arena is 2d matrix, 1 based indexing,
    ### where value at ant_arena[i][j] is amount of pheromone
    ### and -1 if no pheromone
    for i in range(1,len(pheromone_graph)):
        for j in range(1,len(pheromone_graph)):
            pheromone_graph[i][j]=pheromone_graph[i][j]*(1-evaporation_parameter)
    return pheromone_graph
