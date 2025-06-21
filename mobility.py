import constants
import math
import random

directions = [[0,1,2,3],              [0,1,3,2],              [0,2,1,3],              [0,2,3,1],
              [0,3,1,2],              [0,3,2,1],              [1,0,2,3],              [1,0,3,2],
              [1,2,0,3],              [1,2,3,0],              [1,3,0,2],              [1,3,2,0],
              [2,0,1,3],              [2,0,3,1],              [2,1,0,3],              [2,1,3,0],
              [2,3,0,1],              [2,3,1,0],              [3,0,1,2],              [3,0,2,1],
              [3,1,0,2],              [3,1,2,0],              [3,2,0,1],              [3,2,1,0]]
              
              
### discrete time based - 1 unit interval
def out_of_boundary(x,y):
    if x>=0 and x<=constants.LENGTH and y>=0 and y<=constants.BREADTH:
        return 0
    return 1
    
def check(x,x_inc,y,y_inc,direction):
    if direction == 1 and not out_of_boundary(x+x_inc,y+y_inc):
        return [x+x_inc,y+y_inc]
    
    if direction == 0 and not out_of_boundary(x-x_inc,y-y_inc):
        return [x-x_inc,y-y_inc]
    
    if direction == 2 and not out_of_boundary(x+x_inc,y-y_inc):
        return [x+x_inc,y-y_inc]
    
    if direction == 3 and not out_of_boundary(x-x_inc,y+y_inc):
        return [x-x_inc,y+y_inc]
    
    return -1

def move_cell(cell):###[x,y]
    x=cell[0]
    y=cell[1]
    m = -math.tan(random.random()*math.pi)
    dist = constants.MOBILE_NODE_SPEED*constants.DISCRETE_TIME_UNIT
    x_inc = dist/(m*m+1)**0.5
    y_inc = dist*m/(1+m*m)**0.5

    random_direction = directions[(int)(random.random()*24)]
    for i in random_direction:
        movable = check(x,x_inc,y,y_inc,i)
        if movable!=-1:
            return movable
    
    return [random.random()*constants.LENGTH,random.random()*constants.BREADTH]
    
    
def move_mobile_nodes(graph):
    for i in range(len(graph)):
        graph[i]=move_cell(graph[i])
        
    return graph
    
    
