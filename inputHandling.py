import time
import pygame
import numpy as np

import utilities

# ----------------------------------------
# Event and input handling
# ----------------------------------------

def handleInputs(simVars):

    timestamp = time.time()
    delta_time = timestamp - simVars["input_timestamp"]

    step = 1 * delta_time

    handleEvents(simVars, step)
    debugHandler(simVars, step)
    movementHandler(simVars, step)
    rotationHandler(simVars, step)

    # Log the input handler time for this frame
    if simVars["enable_logging"]:
        simVars["log"]["input_handler_time"].append(time.time() - timestamp)

    # Update the input timestamp (storing this frame's timestamp)
    simVars["input_timestamp"] = timestamp

def handleEvents(simVars, step):

    for event in pygame.event.get():
        # A quit event does not warrant a plot. It is a request for immediate termination
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.VIDEORESIZE:
            utilities.updateVarsOnResize(simVars)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                simVars["running"] = False
            if event.key == pygame.K_SPACE:
                simVars["show_overlay"] = not simVars["show_overlay"]
            if event.key == pygame.K_p:
                simVars["render_mode"] = "points"
            if event.key == pygame.K_o:
                simVars["render_mode"] = "wireframe"
            if event.key == pygame.K_i:
                simVars["render_mode"] = "solid"
            if event.key == pygame.K_EQUALS:
                if pygame.mouse.get_visible():
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                else:
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)

def movementHandler(simVars, step):

    keys = pygame.key.get_pressed()

    # Calculate camera direction vector
    dir_vec3 = np.array([np.sin(simVars["cameraRot"][1]), -np.sin(simVars["cameraRot"][0]), -np.cos(simVars["cameraRot"][1])])

    # Normalize direction vector
    length = np.sqrt(dir_vec3[0]**2 + dir_vec3[1]**2 + dir_vec3[2]**2)
    dir_vec3 /= length

    # Calculate up vector
    up_vec3 = np.array([0, 1, 0])

    # Calculate strafe vector using cross product
    strafe_vec3 = np.cross(dir_vec3, up_vec3)

    # Normalize strafe vector
    length = np.sqrt(strafe_vec3[0]**2 + strafe_vec3[1]**2 + strafe_vec3[2]**2)
    strafe_vec3 /= length

    

    if keys[pygame.K_s]:
        simVars["cameraCoords"] += dir_vec3 * step
    if keys[pygame.K_z]:
        simVars["cameraCoords"] -= dir_vec3 * step
    if keys[pygame.K_q]:
        simVars["cameraCoords"] -= strafe_vec3 * step
    if keys[pygame.K_d]:
        simVars["cameraCoords"] += strafe_vec3 * step
    if keys[pygame.K_e]:
        simVars["cameraCoords"][1] += step
    if keys[pygame.K_a]:
        simVars["cameraCoords"][1] -= step

def rotationHandler(simVars, step):

    mouse_move = pygame.mouse.get_rel()

    simVars["cameraRot"][0] -= mouse_move[1]/100
    simVars["cameraRot"][1] -= mouse_move[0]/100

def debugHandler(simVars, step):
    keys = pygame.key.get_pressed()

    # Increase and decrease fov
    if keys[pygame.K_m]:
        simVars["fov"] -= step
        simVars["projection_matrix"] = utilities.getProjectionMatrix(simVars)
    if keys[pygame.K_l]:
        simVars["fov"] += step
        simVars["projection_matrix"] = utilities.getProjectionMatrix(simVars)
    
    # Incresae and decrease Y value of all points' poisitions
    if keys[pygame.K_DOWN] or keys[pygame.K_UP]:
        for i in range(len(simVars["gameObjects"])):
            object = simVars["gameObjects"][i]
            for j in range(len(object["points"])):
                if keys[pygame.K_DOWN]:
                    object["points"][j][1] -= step
                if keys[pygame.K_UP]:
                    object["points"][j][1] += step

    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        # Rotate camera on z axis
        if keys[pygame.K_LEFT]:
            simVars["cameraRot"][2] -= step
        if keys[pygame.K_RIGHT]:
            simVars["cameraRot"][2] += step