import sys
import random
import constants
import ACO_MWSN
import time
import fileTrans
import mobility
import os
import animation_functions
import pygame

def path_to_coordinates(path,graph_node,graph_robot):
    ret = []
    for i in range(len(path)):
        node=path[i]
        if node>0:
            ret += [ [graph_node[node][0],graph_node[node][1]]  ]
        else:
            ret += [ [graph_robot[-node][0],graph_robot[-node][1]]  ]
    return ret


mobile_robot_count = constants.MOBILE_ROBOT_COUNT
mobile_robot_speed = constants.MOBILE_ROBOT_SPEED
mobile_node_count = constants.MOBILE_NODE_COUNT
mobile_node_speed = constants.MOBILE_NODE_SPEED
base_station_x = constants.BASE_STATION_X
base_station_y = constants.BASE_STATION_Y

window = pygame.display.set_mode((constants.BREADTH, constants.LENGTH)) #GraphWin('MWSN',constants.BREADTH, constants.LENGTH)
pygame.display.set_caption("Wireless Sensor Network - Any colony optiimization")

#win = Windows
screen  = pygame.surface.Surface((constants.BREADTH, constants.LENGTH))
screen.fill(constants.BACKGROUND_COLOR)
window.blit(screen, (0,0))
pygame.display.flip()

### initialize graph_node and graph_robot with random initial coordinates
graph_node = [[random.random()*(constants.LENGTH+1),random.random()*(constants.BREADTH+1)] for i in range(constants.MOBILE_NODE_COUNT+1) ]
graph_robot = [[random.random()*(constants.LENGTH+1),random.random()*(constants.BREADTH+1)] for i in range(constants.MOBILE_ROBOT_COUNT+1) ]

start_time = time.time()

while time.time()-start_time <= constants.SIMULATION_TIME:
        ## introduce mobility
        graph_node = mobility.move_mobile_nodes(graph_node)
        
        #//# draw on win the mobile_nodes and mobile_robots
        animation_functions.plot_mobile_nodes(graph_node, screen, window)
        animation_functions.plot_mobile_robots(graph_robot, screen, window)
        
        ## graph = create_dist_graph(graph_node)
        dist_graph = [ [-1 for i in range(mobile_node_count+1) ] for j in range(mobile_node_count+1) ]
        for i in range(1,len(graph_node)):
                for j in range(1,len(graph_node)):
                        distance = ((graph_node[i][0]-graph_node[j][0])**2+(graph_node[i][1]-graph_node[j][1])**2)**0.5
                        if i!=j:# and distance<=constants.RANGE_RADIUS:
                                dist_graph[i][j]=distance                              
        
        ## choose nodes for transmission
        sender = 1+(int)(random.random()*(constants.MOBILE_NODE_COUNT))
        receiver = sender
        while receiver == sender:
                receiver = 1+(int)(random.random()*(constants.MOBILE_NODE_COUNT))        
        
        ## get optimal/suboptimal_path using ACO
        path = ACO_MWSN.get_path(sender,receiver,dist_graph)

        #//# draw ACO path on win
        path_points = path_to_coordinates(path,graph_node,graph_robot)
        animation_functions.draw_path(path_points,2,screen, window)
        
        print ("Sender ",sender)
        print ("Receiver ",receiver)

        ## write path to file
        fileTrans.path_to_file("ACOPath.txt",path)
        
        flag = 0
        while flag==0:
                flag = fileTrans.ACO_path_to_console("ACOPath.txt")
                  
        ## write mobile node coordinates & robotic nodes coordinates
        fileTrans.coordintes_to_file("MobileNode.txt",graph_node)
        fileTrans.coordintes_to_file("MobileRobot.txt",graph_robot)

        file_=open("ReinforcementFlag.txt","w")
        file_.close()
                
        local_time = time.time()
        flag=1
        while time.time() - local_time <=constants.DISCRETE_TIME_UNIT:
                flag = fileTrans.is_not_true("ReinforcementFlag.txt")
                if flag == 0:
                        break
                ## c++ code run reinforcement
                os.system("link_reinforcement.exe")

                ## we try to send packets through same link
                ## till need for reinforcement arises
                ## in case of which, we look for flag.txt file, if it contains TRUE, it means the link was reinforced,
                ## and we terminated from inner loop
                ## otherwise we continue the inner loop till DISCRETE_TIME_UNIT
                
                ####output = check_and_reinforce(path) >>>>>>>>>>>>>>>>>>
                time.sleep(constants.DELAY_PER_CYCLE)
        if flag == 0:
                while flag==0:
                        flag_path = fileTrans.reinforce_path_to_console("UpdatedPath.txt")### this is reinforced path file
                        flag = flag_path[0]
                #//# draw reinforced path on win after clearing all previous frames
                animation_functions.delete(screen, window)
                #//#changes values
                path_to_plot = flag_path[1]
                print(list(path_to_plot))
                for i in range(len(path_to_plot)):
                        if path_to_plot[i]<0:
                                previous_node = path_to_plot[i-1]
                                neg_number = path_to_plot[i]
                                next_node = path_to_plot[i+1]
                                
                previous_node_x = graph_node[previous_node][0]
                previous_node_y = graph_node[previous_node][1]
                next_node_x = graph_node[next_node][0]
                next_node_y = graph_node[next_node][1]
                
                graph_robot[-neg_number][0]=(previous_node_x+next_node_x)/2
                graph_robot[-neg_number][1]=(previous_node_y+next_node_y)/2
                
                #//# draw graph nodes, graph robots
                animation_functions.plot_mobile_nodes(graph_node,screen, window)
                animation_functions.plot_mobile_robots(graph_robot,screen, window)
                
                path_points = path_to_coordinates(flag_path[1],graph_node,graph_robot)
                animation_functions.draw_path(path_points,2,screen, window)
                        
        else:
                print ("Path remained intact without need for reinforcement for ",constants.DISCRETE_TIME_UNIT,"(s) duration")
                
        print ("*************** ONE DISCRETE TIME UNIT COMPLETED  ***************")
        time.sleep(constants.DELAY_PER_CYCLE)
        
        animation_functions.delete(screen, window)  
        