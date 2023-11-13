import pygame
import time
import math
import numpy as np

import simulation_py.config as config
import simulation_py.utilities as utilities

# ----------------------------------------
# Drawing functions
# ----------------------------------------


def handleDisplay(simVars, screen):

    # Get the current time and calculate the time since the last frame
    timestamp = time.time()
    delta_time = timestamp - simVars["display_timestamp"]
    # If the time since the last frame is less than the target frame time, don't render
    if (delta_time < 1/config.FPS):
        return

    # Clear the screen
    screen.fill(config.COLOR_BG)

    # Draw the grid
    #drawGrid(simVars, screen)

    # Draw the points
    drawWorld(simVars, screen)
    # Draw the overlay
    if (simVars["show_overlay"]):
        drawOverlay(simVars, screen)

    # Apply changes to screen
    pygame.display.flip()

    if simVars["enable_logging"]:
        # Log the render time for this frame
        simVars["log"][simVars["render_mode"]]["render_time"].append(
            time.time() - timestamp)
        # Updating these values every frame is not optimal
        simVars["log"][simVars["render_mode"]
                       ]["rendered_points"] = simVars["log"][simVars["render_mode"]]["rendered_points"]
        simVars["log"][simVars["render_mode"]
                       ]["rendered_faces"] = simVars["log"][simVars["render_mode"]]["rendered_faces"]
        simVars["frame_nb"] += 1
        if simVars["frame_nb"] == config.LOG_NB_FRAMES or timestamp - simVars["start_timestamp"] > config.LOG_MAX_TIME:
            simVars["log"][simVars["render_mode"]
                           ]["test_time"] = timestamp - simVars["start_timestamp"]
            simVars["start_timestamp"] = timestamp
            simVars["frame_nb"] = 0
            match simVars["render_mode"]:
                case "points":
                    simVars["render_mode"] = "wireframe"
                case "wireframe":
                    simVars["render_mode"] = "solid"
                case "solid":
                    simVars["running"] = False

    # Update the fps timestamp (storing this frame's timestamp)
    simVars["display_timestamp"] = timestamp


def drawWorld(simVars, screen):

    # Math out this frame's camera rotation matrix
    camera_rotation_matrix = utilities.getCameraRotationMatrix(simVars["cameraRot"])

    # Math out the 3d points on the canvas (1 unit away from the camera)
    if (simVars["render_mode"] == "points"):
        simVars["log"]["points"]["rendered_points"] = 0
        simVars["log"]["points"]["rendered_faces"] = 0
        for object in simVars["gameObjects"]:
            for point in object["points"]:
                point_2D = utilities.vec3tovec2(simVars, point, camera_rotation_matrix)
                color = utilities.getColor(simVars, point)

                if point_2D == (-1, -1):
                    continue

                # Draw the point
                pygame.draw.circle(screen, color, point_2D, 3)

    elif (simVars["render_mode"] == "wireframe"):
        simVars["log"]["wireframe"]["rendered_points"] = 0
        simVars["log"]["wireframe"]["rendered_faces"] = 0
        for object in simVars["gameObjects"]:
            pre_baked_points = []
            pre_baked_colors = []
            for point in object["points"]:
                pre_baked_points.append(utilities.vec3tovec2(simVars, point, camera_rotation_matrix))
                pre_baked_colors.append(utilities.getColor(simVars, point))

            for face in object["faces"]:

                if pre_baked_points[face[0] - 1] == (-1, -1) or pre_baked_points[face[1] - 1] == (-1, -1) or pre_baked_points[face[2] - 1] == (-1, -1):
                    continue

                face_2D = [
                    pre_baked_points[face[0] - 1],
                    pre_baked_points[face[1] - 1],
                    pre_baked_points[face[2] - 1]]
                colors = [
                    pre_baked_colors[face[0] - 1],
                    pre_baked_colors[face[1] - 1],
                    pre_baked_colors[face[2] - 1]
                ]

                pygame.draw.line(screen, colors[0], face_2D[0], face_2D[1], 1)
                pygame.draw.line(screen, colors[1], face_2D[1], face_2D[2], 1)
                pygame.draw.line(screen, colors[2], face_2D[2], face_2D[0], 1)

    elif (simVars["render_mode"] == "solid"):

        simVars["log"]["solid"]["rendered_points"] = 0
        simVars["log"]["solid"]["rendered_faces"] = 0

        # 12 colors
        colors = [
            (255, 0, 0),
            (255, 127, 0),
            (255, 255, 0),
            (127, 255, 0),
            (0, 255, 0),
            (0, 255, 127),
            (0, 255, 255),
            (0, 127, 255),
            (0, 0, 255),
            (127, 0, 255),
            (255, 0, 255),
            (255, 0, 127)
        ]
        for object in simVars["gameObjects"]:
            
            for i, face in enumerate(object["faces"]):
                normal = utilities.getFaceNormal(simVars, [
                    object["points"][face[0] - 1],
                    object["points"][face[1] - 1],
                    object["points"][face[2] - 1]
                ])
                if (object["points"][face[0] - 1][0] - simVars["cameraCoords"][0]) * normal[0] + (object["points"][face[0] - 1][1] - simVars["cameraCoords"][1]) * normal[1] + (object["points"][face[0] - 1][2] - simVars["cameraCoords"][2]) * normal[2] < 0:                                        
                    
                    face_2D = [
                        utilities.vec3tovec2(simVars, object["points"][face[0] - 1], camera_rotation_matrix),
                        utilities.vec3tovec2(simVars, object["points"][face[1] - 1], camera_rotation_matrix),
                        utilities.vec3tovec2(simVars, object["points"][face[2] - 1], camera_rotation_matrix)
                    ]

                    if face_2D[0] == (-1, -1) or face_2D[1] == (-1, -1) or face_2D[2] == (-1, -1):
                        continue

                    #color = utilities.getColor(simVars, object["points"][face[0] - 1])
                    color = colors[i%12]
                    # Color gradient not implemented
                    simVars["log"]["solid"]["rendered_faces"] += 1
                    pygame.draw.polygon(screen, color, face_2D)

def drawGrid(simVars, screen):
    x_limits = [-5, 5]
    z_limits = [-5, 5]

    # Draw the grid
    for i in range(x_limits[0], x_limits[1] + 1):
        point_s = [x_limits[0], 0, i]
        point_e = [x_limits[1], 0, i]
        coords_s = utilities.vec3tovec2(simVars, point_s)
        coords_e = utilities.vec3tovec2(simVars, point_e)
        color = (255, 255, 255)
        pygame.draw.line(screen, color, coords_s, coords_e, 1)

    for i in range(z_limits[0], z_limits[1] + 1):
        point_s = [i, 0, z_limits[0]]
        point_e = [i, 0, z_limits[1]]
        coords_s = utilities.vec3tovec2(simVars, point_s)
        coords_e = utilities.vec3tovec2(simVars, point_e)
        color = (255, 255, 255)
        pygame.draw.line(screen, color, coords_s, coords_e, 1)


def drawOverlay(simVars, screen):
    font = pygame.font.SysFont("Roboto", 30)

    overlay_w = simVars["overlay_size"][0]
    overlay_h = simVars["overlay_size"][1]

    hud = pygame.Surface((overlay_w, overlay_h), pygame.SRCALPHA)

    pygame.draw.rect(hud, simVars["color_overlay_bg"],
                     (0, 0, overlay_w, overlay_h), 0, 10)
    pygame.draw.rect(hud, simVars["color_overlay_border"],
                     (0, 0, overlay_w, overlay_h), 2, 10)

    # Overlay content
    text = []

    frame_time = time.time() - simVars["display_timestamp"]

    text.append(font.render("n° of points: " +
                str(simVars["log"][simVars["render_mode"]]["rendered_points"]), True, simVars["color_overlay_txt"]))
    text.append(font.render("n° of faces: " +
                str(simVars["log"][simVars["render_mode"]]["rendered_faces"]), True, simVars["color_overlay_txt"]))
    text.append(font.render("FPS: " + str(round(1/frame_time, 5)),
                True, simVars["color_overlay_txt"]))
    text.append(font.render(
        "Camera: " + str([round(num, 2) for num in simVars["cameraCoords"]]), True, simVars["color_overlay_txt"]))
    text.append(font.render(
        "Camera rotation: " + str([round(np.degrees(num), 2) for num in simVars["cameraRot"]]), True, simVars["color_overlay_txt"]))
    text.append(font.render(
        "Frames: " + str(simVars["frame_nb"]), True, simVars["color_overlay_txt"]))
    text.append(font.render("Runtime: " + str(round(time.time() -
                simVars["start_timestamp"], 3)), True, simVars["color_overlay_txt"]))
    # FOV
    text.append(font.render("FOV: " + str(round(simVars["fov"], 2)),
                True, simVars["color_overlay_txt"]))

    for i in range(len(text)):
        rect = text[i].get_rect(
            centery=((i+1)*overlay_h/(len(text)+1)), left=10)
        hud.blit(text[i], rect)

    screen.blit(hud, simVars["overlay_pos"])