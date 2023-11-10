import pygame
import config
import numpy as np
import math


def updateVarsOnResize(simVars):
    simVars["resolution"] = pygame.display.get_surface().get_size()
    simVars["overlay_size"] = (config.OVERLAY_SIZE[0]/100 * simVars["resolution"]
                               [0], config.OVERLAY_SIZE[1]/100 * simVars["resolution"][1])
    simVars["overlay_pos"] = (config.OVERLAY_POS[0]/100 * simVars["resolution"]
                              [0], config.OVERLAY_POS[1]/100 * simVars["resolution"][1])
    simVars["projection_matrix"] = getProjectionMatrix(simVars)


def getProjectionMatrix(simVars):
    # Create projection matrix
    nearClip = simVars["nearClip"]
    farClip = simVars["farClip"]
    fov = simVars["fov"]
    aspect_ratio = simVars["resolution"][0] / simVars["resolution"][1]

    projection_matrix = np.array([
        [1/(aspect_ratio * math.tan(fov/2)), 0, 0, 0],
        [0, 1/(math.tan(fov/2)), 0, 0],
        [0, 0, (farClip + nearClip)/(farClip - nearClip),
         (-2 * farClip * nearClip)/(farClip - nearClip)],
        [0, 0, 1, 0]
    ])

    return projection_matrix


def vec3tovec2(simVars, point):
        
    resolution = simVars["resolution"]
    ratio = resolution[0]/resolution[1]
    camera = simVars["cameraCoords"]
    rotation = simVars["cameraRot"]

    # rotation matrices. Apply rotation to the point (in respect to world origin):

    cos_y = math.cos(rotation[1])
    sin_y = math.sin(rotation[1])
    cos_z = math.cos(rotation[2])
    sin_z = math.sin(rotation[2])
    cos_x = math.cos(rotation[0])
    sin_x = math.sin(rotation[0])

    rotation_matrix = np.array([
            [cos_z * cos_y, cos_z * sin_y * sin_x - sin_z * cos_x, cos_z * sin_y * cos_x + sin_z * sin_x],
            [sin_z * cos_y, sin_z * sin_y * sin_x + cos_z * cos_x, sin_z * sin_y * cos_x - cos_z * sin_x],
            [-sin_y, cos_y * sin_x, cos_y * cos_x],
            ])
    point = np.array(point)
    point = np.matmul(rotation_matrix, point)

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