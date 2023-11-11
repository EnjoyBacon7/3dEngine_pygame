import time
import pygame
import numpy as np

import utilities


# ----------------------------------------
# Event and input handling
# ----------------------------------------


def handleEvents(simVars):

    timestamp = time.time()
    delta_time = timestamp - simVars["input_timestamp"]

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

    # Calculate direction vector
    dirX = np.sin(simVars["cameraRot"][1])
    dirY = -np.sin(simVars["cameraRot"][0])
    dirZ = -np.cos(simVars["cameraRot"][1])

    # Normalize direction vector
    length = np.sqrt(dirX**2 + dirY**2 + dirZ**2)
    dirX /= length
    dirY /= length
    dirZ /= length

    # Calculate up vector
    upX, upY, upZ = 0, 1, 0

    # Calculate strafe vector using cross product
    strafeX = dirY*upZ - dirZ*upY
    strafeY = dirZ*upX - dirX*upZ
    strafeZ = dirX*upY - dirY*upX

    # Normalize strafe vector
    length = np.sqrt(strafeX**2 + strafeY**2 + strafeZ**2)
    strafeX /= length
    strafeY /= length
    strafeZ /= length


    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        simVars["cameraCoords"][0] += dirX * 1*delta_time
        simVars["cameraCoords"][1] += dirY * 1*delta_time
        simVars["cameraCoords"][2] += dirZ * 1*delta_time
    if keys[pygame.K_z]:
        simVars["cameraCoords"][0] -= dirX * 1*delta_time
        simVars["cameraCoords"][1] -= dirY * 1*delta_time
        simVars["cameraCoords"][2] -= dirZ * 1*delta_time
    if keys[pygame.K_q]:
        simVars["cameraCoords"][0] -= strafeX * 1*delta_time
        simVars["cameraCoords"][1] -= strafeY * 1*delta_time
        simVars["cameraCoords"][2] -= strafeZ * 1*delta_time
    if keys[pygame.K_d]:
        simVars["cameraCoords"][0] += strafeX * 1*delta_time
        simVars["cameraCoords"][1] += strafeY * 1*delta_time
        simVars["cameraCoords"][2] += strafeZ * 1*delta_time
    if keys[pygame.K_m]:
        # Lower fov
        simVars["fov"] -= 1 * delta_time
        simVars["projection_matrix"] = utilities.getProjectionMatrix(simVars)
    if keys[pygame.K_l]:
        # Increase fov
        simVars["fov"] += 1 * delta_time
        simVars["projection_matrix"] = utilities.getProjectionMatrix(simVars)
    if keys[pygame.K_e]:
        simVars["cameraCoords"][1] += 1*delta_time
    if keys[pygame.K_a]:
        simVars["cameraCoords"][1] -= 1*delta_time
    if keys[pygame.K_b]:
        simVars["scale"] += 1
    if keys[pygame.K_n]:
        simVars["scale"] -= 1
    # test buttons
    if keys[pygame.K_DOWN] or keys[pygame.K_UP]:
        for i in range(len(simVars["gameObjects"])):
            object = simVars["gameObjects"][i]
            for j in range(len(object["points"])):
                if keys[pygame.K_DOWN]:
                    object["points"][j][1] -= 0.05
                if keys[pygame.K_UP]:
                    object["points"][j][1] += 0.05
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        # Rotate camera on z axis
        if keys[pygame.K_LEFT]:
            simVars["cameraRot"][2] -= 0.0005
        if keys[pygame.K_RIGHT]:
            simVars["cameraRot"][2] += 0.0005

    mouse_move = pygame.mouse.get_rel()

    simVars["cameraRot"][0] -= mouse_move[1]/100
    simVars["cameraRot"][1] -= mouse_move[0]/100

    # Log the input handler time for this frame
    if simVars["enable_logging"]:
        simVars["log"]["input_handler_time"].append(time.time() - timestamp)

    # Update the input timestamp (storing this frame's timestamp)
    simVars["input_timestamp"] = timestamp