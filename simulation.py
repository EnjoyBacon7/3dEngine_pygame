import pygame
import config
import utilities
import math

# ----------------------------------------
# Initialise the simulation
# ----------------------------------------


def init():
    simVars = {
        # World composition
        "gameObjects": [],

        # Camera variables
        "cameraCoords": [0, 0, -5],
        "cameraRot": [0, 0, 0],
        "fov": 90,
        "farClip": [100],
        "nearClip": [1],
        "scale": config.SCALE,

        # Loading variables from config.py
        "resolution": config.RESOLUTION,
        "overlay_size": (config.OVERLAY_SIZE[0]/100 * config.RESOLUTION[0], config.OVERLAY_SIZE[1]/100 * config.RESOLUTION[1]),
        "overlay_pos": (config.OVERLAY_POS[0]/100 * config.RESOLUTION[0], config.OVERLAY_POS[1]/100 * config.RESOLUTION[1]),
        "color_overlay_bg": config.COLOR_OVERLAY_BG,
        "color_overlay_border": config.COLOR_OVERLAY_BORDER,
        "color_overlay_txt": config.COLOR_OVERLAY_TXT,
        "color_points": config.COLOR_POINTS,
        "hide_overlay": config.HIDE_OVERLAY,

        # Rendering variables
        "render_mode": "solid",  # "wireframe", "solid", or "points"

        "clock": pygame.time.Clock(),

        # Logging variables
        "log": {
            "rendered_points": 0,
            "rendered_faces": 0,
        }
    }
    return simVars

# ----------------------------------------
# Main loop
# ----------------------------------------


def loop(simVars, screen):

    running = True
    while running:

        # Handle input and events
        handleEvents(simVars)
        # Display on screen
        handleDisplay(simVars, screen)
        # Limit fps
        simVars["clock"].tick(120)

# ----------------------------------------
# Event and input handling
# ----------------------------------------


def handleEvents(simVars):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.VIDEORESIZE:
            utilities.updateVarsOnResize(simVars)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_SPACE:
                simVars["hide_overlay"] = not simVars["hide_overlay"]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        simVars["cameraCoords"][2] -= 0.05
    if keys[pygame.K_z]:
        simVars["cameraCoords"][2] += 0.05
    if keys[pygame.K_q]:
        simVars["cameraCoords"][0] -= 0.05
    if keys[pygame.K_d]:
        simVars["cameraCoords"][0] += 0.05
    if keys[pygame.K_e]:
        simVars["cameraCoords"][1] += 0.05
    if keys[pygame.K_a]:
        simVars["cameraCoords"][1] -= 0.05
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
                    object["points"][j] -= 0.05
                if keys[pygame.K_UP]:
                    object["points"][j] += 0.05

    mouse_move = pygame.mouse.get_rel()
    simVars["cameraRot"][0] += mouse_move[1]/100
    simVars["cameraRot"][1] += mouse_move[0]/100

# ----------------------------------------
# Drawing functions
# ----------------------------------------


def handleDisplay(simVars, screen):

    # Clear the screen
    screen.fill(config.COLOR_BG)

    # Draw the grid
    # drawGrid(simVars, screen)

    # Draw the points
    drawWorld(simVars, screen)
    # Draw the overlay
    if (not simVars["hide_overlay"]):
        drawOverlay(simVars, screen)

    # Apply changes to screen
    pygame.display.flip()


def drawWorld(simVars, screen):

    simVars["log"]["rendered_points"] = 0
    simVars["log"]["rendered_edges"] = 0
    simVars["log"]["rendered_faces"] = 0

    # Math out the 3d points on the canvas (1 unit away from the camera)
    if (simVars["render_mode"] == "wireframe"):
        for object in simVars["gameObjects"]:
            for face in object["faces"]:
                face_2D = [
                    utilities.vec3tovec2(simVars, object["points"][face[0] - 1]),
                    utilities.vec3tovec2(simVars, object["points"][face[1] - 1]),
                    utilities.vec3tovec2(simVars, object["points"][face[2] - 1]),
                ]
                colors = [
                    utilities.getColor(simVars, object["points"][face[0] - 1]),
                    utilities.getColor(simVars, object["points"][face[1] - 1]),
                    utilities.getColor(simVars, object["points"][face[2] - 1]),
                ]

                simVars["log"]["rendered_points"] += 3
                pygame.draw.line(screen, colors[0], face_2D[0], face_2D[1])
                pygame.draw.line(screen, colors[1], face_2D[1], face_2D[2])
                pygame.draw.line(screen, colors[2], face_2D[2], face_2D[0])

    elif (simVars["render_mode"] == "solid"):
        for i in range(len(simVars["gameObjects"])):
            object = simVars["gameObjects"][i]
            for j in range(len(object["faces"])):
                face = object["faces"][j]
                face_2D = [
                    utilities.vec3tovec2(simVars, object["points"][face[0] - 1]),
                    utilities.vec3tovec2(simVars, object["points"][face[1] - 1]),
                    utilities.vec3tovec2(simVars, object["points"][face[2] - 1]),
                ]
                color = utilities.getColor(simVars, object["points"][face[0] - 1])

                simVars["log"]["rendered_points"] += 3
                simVars["log"]["rendered_faces"] += 1
                pygame.draw.polygon(screen, color, face_2D)

    elif (simVars["render_mode"] == "points"):
        for i in range(len(simVars["gameObjects"])):
            object = simVars["gameObjects"][i]
            for j in range(len(object["points"])):
                point_2D = utilities.vec3tovec2(simVars, object["points"][j])
                color = utilities.getColor(simVars, object["points"][j])

                # Draw the point
                simVars["log"]["rendered_points"] += 1
                pygame.draw.circle(screen, color, point_2D, 3)


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

    text.append(font.render("n° of points: " + str(simVars["log"]["rendered_points"]), True, simVars["color_overlay_txt"]))
    text.append(font.render("n° of faces: " + str(simVars["log"]["rendered_faces"]), True, simVars["color_overlay_txt"]))
    text.append(font.render("FPS: " + str(round(simVars["clock"].get_fps(), 2)), True, simVars["color_overlay_txt"]))
    text.append(font.render("Camera: " + str([round(num, 2) for num in simVars["cameraCoords"]]), True, simVars["color_overlay_txt"]))


    for i in range(len(text)):
        rect = text[i].get_rect(centery=((i+1)*overlay_h/(len(text)+1)), left=10)
        hud.blit(text[i], rect)

    screen.blit(hud, simVars["overlay_pos"])
