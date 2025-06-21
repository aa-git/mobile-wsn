import pygame
import constants
import time
import mobility
import random


def draw_cell(x,y,r,fill_color,line_color, window, screen):
    pygame.draw.circle(window, fill_color, (x,y), r)
    # cir = Circle(Point(x,y),r)
    # cir.draw(win)
    # cir.setFill(fill_color)
    # cir.setOutline(line_color)
    # return win
    
def line(x1,y1,x2,y2,width,window, screen):
    pygame.draw.line(window, (0,0,0), (x1,y1), (x2,y2))
    ## all lines with black color

    # line = Line(Point(x1,y1), Point(x2,y2))
    # line.setWidth(width)
    # line.draw(win)
    # return win

def draw_path(path,width, window, screen):
    for i in range(len(path)-1):
        x1=path[i][0]
        y1=path[i][1]

        x2=path[i+1][0]
        y2=path[i+1][1]
        
        line(x1,y1,x2,y2, width, window, screen)

    screen.blit(window, (0,0))
    pygame.display.update()
    #return win
    
def plot_mobile_nodes(graph, window, screen):
    for i in range(1,len(graph)):
        x=graph[i][0]
        y=graph[i][1]
        draw_cell(x,
                  y,
                  constants.MOBILE_NODE_RADIUS,
                  constants.MOBILE_NODE_FILL_COLOR,
                  constants.MOBILE_NODE_OUTLINE_COLOR,
                  window, screen)
    screen.blit(window, (0,0))
    pygame.display.update()
    #return win
        
def plot_mobile_robots(graph,window, screen):
    for i in range(1,len(graph)):
        x=graph[i][0]
        y=graph[i][1]
        draw_cell(x,
                  y,
                  constants.MOBILE_ROBOT_RADIUS,
                  constants.MOBILE_ROBOT_FILL_COLOR,
                  constants.MOBILE_ROBOT_OUTLINE_COLOR,
                  window, screen)
    #return win

def delete(window, screen):
    # window  = pygame.surface.Surface((constants.BREADTH, constants.LENGTH))
    # window.fill(constants.BACKGROUND_COLOR)
    # screen.blit(window, (0,0))
    screen.fill(constants.BACKGROUND_COLOR)
    window.fill(constants.BACKGROUND_COLOR)
    window.blit(screen, (0,0))
    pygame.display.update()