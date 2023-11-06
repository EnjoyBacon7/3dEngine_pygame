import pygame
import config
import numpy as np
import math

def updateVarsOnResize(simVars):
    simVars["resolution"] = pygame.display.get_surface().get_size()
    simVars["overlay_size"] = (config.OVERLAY_SIZE[0]/100 * simVars["resolution"][0], config.OVERLAY_SIZE[1]/100 * simVars["resolution"][1])
    simVars["overlay_pos"] = (config.OVERLAY_POS[0]/100 * simVars["resolution"][0], config.OVERLAY_POS[1]/100 * simVars["resolution"][1])

def vec3tovec2(simVars, point):
        
        resolution = simVars["resolution"]
        ratio = resolution[0]/resolution[1]
        camera = simVars["cameraCoords"]
        rotation = simVars["cameraRot"]

        # rotation matrices. Apply rotation to the point (in respect to world origin):

        x_rotation = np.array([[1, 0, 0],
                               [0, math.cos(rotation[0]), -math.sin(rotation[0])],
                               [0, math.sin(rotation[0]), math.cos(rotation[0])]])
        y_rotaiton = np.array([[math.cos(rotation[1]), 0, math.sin(rotation[1])],
                               [0, 1, 0],
                               [-math.sin(rotation[1]), 0, math.cos(rotation[1])]])
        z_rotation = np.array([[math.cos(rotation[2]), -math.sin(rotation[2]), 0],
                               [math.sin(rotation[2]), math.cos(rotation[2]), 0],
                               [0, 0, 1]])


        # Apply rotation matrices to the point
        point = np.array(point)
        point = np.matmul(x_rotation, point)
        point = np.matmul(y_rotaiton, point)
        point = np.matmul(z_rotation, point)

        # For both axes :
        # x - cameraX (input camera movement)
        # / (z - cameraZ) Thales theorem
        # * ratio (to keep the ratio on resize)
        # * 300 (to scale up the points) //// 300 is arbitrary

        if point[2] - camera[2] == 0:
            relative_x = 0
            relative_y = 0
        elif(point[2] - camera[2] < 0):
            screen_x = -1
            screen_y = -1
            return (screen_x, screen_y)
        else:
            relative_x = (point[0] - camera[0])/(point[2] - camera[2])
            relative_y = (point[1] - camera[1])/(-(point[2] - camera[2]))

        screen_x = relative_x * ratio * simVars["scale"] + resolution[0]/2
        screen_y = relative_y * ratio * simVars["scale"] + resolution[1]/2

        simVars["log"][simVars["render_mode"]]["rendered_points"] += 1

        return (screen_x, screen_y)

def getColor(simVars, point):   
    dst_to_origin = math.sqrt(point[0] * point[0] + point[1] * point[1] + point[2] * point[2])
    dst_to_origin = max(min(dst_to_origin, 5), 0)
    ratio = dst_to_origin/5
    r = 255 + ratio * (42 - 255)
    g = ratio * (85 - 0)
    b = ratio * (91 - 0)
    color = (r, g, b)
    return(color)