import pygame
import simulation_py.config as config
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
        [1/(aspect_ratio * math.tan(math.radians(fov)/2)), 0, 0, 0],
        [0, 1/(math.tan(math.radians(fov)/2)), 0, 0],
        [0, 0, (farClip + nearClip)/(farClip - nearClip),
         (-2 * farClip * nearClip)/(farClip - nearClip)],
        [0, 0, 1, 0]
    ])

    return projection_matrix


def vec3tovec2(simVars, point, camera_rotation_matrix):

    # To determine a point's position on the screen:
    # - Express the point's position in camera coordinates
    # - Apply the rotation of the camera
    # - Apply homogenous coordinates
    # - Normalize the 2d vector

    point = np.array(point)

    camera_position = np.array(simVars["cameraCoords"])

    # Apply change of origin and apply orientation
    point = np.matmul(camera_rotation_matrix, (point - camera_position))

    # Apply homogenous coordinates
    point = np.array([point[0], point[1], point[2], 1])

    # Apply projection matrix
    projection_matrix = simVars["projection_matrix"]
    point = np.matmul(projection_matrix, point)

    # Remove points behind the camera
    if point[2] < 0:
        return (-1, -1)

    # Normalize the vector
    point = point / point[3]

    # Remove points outside of NDC space
    if point[0] < -1 or point[0] > 1 or point[1] < -1 or point[1] > 1:
        return(-1, -1)

    # Apply viewport transformation
    point = np.array([point[0] * simVars["resolution"][0]/2, point[1] * simVars["resolution"]
                     [1]/2, point[2] * simVars["resolution"][0]/2, point[3] * simVars["resolution"][1]/2])

    # Apply offset
    screen_x = simVars["resolution"][0]/2 + point[0]
    screen_y = simVars["resolution"][1]/2 - point[1]

    # Add 1 to rendered points
    simVars["log"][simVars["render_mode"]]["rendered_points"] += 1

    return (screen_x, screen_y)


def getColor(simVars, point):
    dst_to_origin = math.sqrt(
        point[0] * point[0] + point[1] * point[1] + point[2] * point[2])
    dst_to_origin = max(min(dst_to_origin, 5), 0)
    ratio = dst_to_origin/5
    r = 255 + ratio * (42 - 255)
    g = ratio * (85 - 0)
    b = ratio * (91 - 0)
    color = (r, g, b)
    return (color)


def getCameraRotationMatrix(camera_orientation):
    cos_x = math.cos(camera_orientation[0])
    sin_x = math.sin(camera_orientation[0])
    cos_y = math.cos(camera_orientation[1])
    sin_y = math.sin(camera_orientation[1])
    cos_z = math.cos(camera_orientation[2])
    sin_z = math.sin(camera_orientation[2])

    Rot_x = np.array([
        [1, 0, 0],
        [0, cos_x, -sin_x],
        [0, sin_x, cos_x]
    ])
    Rot_y = np.array([
        [cos_y, 0, sin_y],
        [0, 1, 0],
        [-sin_y, 0, cos_y]
    ])
    Rot_z = np.array([
        [cos_z, -sin_z, 0],
        [sin_z, cos_z, 0],
        [0, 0, 1]
    ])

    # Full matrix = Rot_x * Rot_y * Rot_z
    rotation_matrix = np.matmul(np.matmul(Rot_x, Rot_y), Rot_z)

    return(rotation_matrix)