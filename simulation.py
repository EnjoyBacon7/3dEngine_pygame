import pygame
import config
import utilities

# ----------------------------------------
# Initialise the simulation
# ----------------------------------------
def init():
    simVars = {
        # World Points
        "points": [],
        "colors": [],

        # Camera variables
        "cameraCoords": [0, 3, -5],
        "fov": 90,
        "farClip": [100],
        "nearClip": [1],

        # Loading variables from config.py
        "resolution": config.RESOLUTION,
        "overlay_size": (config.OVERLAY_SIZE[0]/100 * config.RESOLUTION[0], config.OVERLAY_SIZE[1]/100 * config.RESOLUTION[1]),
        "overlay_pos": (config.OVERLAY_POS[0]/100 * config.RESOLUTION[0], config.OVERLAY_POS[1]/100 * config.RESOLUTION[1]),
        "color_overlay_bg": config.COLOR_OVERLAY_BG,
        "color_overlay_border": config.COLOR_OVERLAY_BORDER,
        "color_overlay_txt": config.COLOR_OVERLAY_TXT,
        "color_points": config.COLOR_POINTS,
        "hide_overlay": config.HIDE_OVERLAY,

        "clock": pygame.time.Clock(),
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
        simVars["clock"].tick(60)

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

# ----------------------------------------
# Drawing functions
# ----------------------------------------
def handleDisplay(simVars, screen):

    camera = simVars["cameraCoords"]
    canvasPoints = []

    # Clear the screen
    screen.fill((0,0,0))

    # Math out the 3d points on the canvas (1 unit away from the camera)
    for i in range(len(simVars["points"])):
        point = simVars["points"][i]
        resolution = simVars["resolution"]
        ratio = resolution[0]/resolution[1]


        # For both axes :
        # x - cameraX (input camera movement)
        # / (z - cameraZ) Thales theorem
        # * ratio (to keep the ratio on resize)
        # * 300 (to scale up the points) //// 300 is arbitrary

        screen_x = (point[0] - camera[0])/(point[2] - camera[2]) * ratio * 300 + resolution[0]/2
        screen_y = (point[1] - camera[1])/(-(point[2] - camera[2])) * ratio * 300 + resolution[1]/2

        coords = [screen_x, screen_y]
        canvasPoints.append(coords)
    
    # Draw the points
    for point in canvasPoints:
        pygame.draw.circle(screen, simVars["color_points"], point, 3)

    # Draw the overlay
    if(not simVars["hide_overlay"]):
        drawOverlay(simVars, screen)

    # Apply changes to screen
    pygame.display.flip()

def drawOverlay(simVars, screen):
    font = pygame.font.SysFont("Roboto", 30)
    points = simVars["points"]

    overlay_w = simVars["overlay_size"][0]
    overlay_h = simVars["overlay_size"][1]

    hud = pygame.Surface((overlay_w, overlay_h), pygame.SRCALPHA)

    pygame.draw.rect(hud, simVars["color_overlay_bg"], (0, 0, overlay_w, overlay_h), 0, 10)
    pygame.draw.rect(hud, simVars["color_overlay_border"], (0, 0, overlay_w, overlay_h), 2, 10)

    text = font.render("Points: " + str(points), True, simVars["color_overlay_txt"])
    text_rect = text.get_rect(center=(overlay_w/2, overlay_h/3))
    hud.blit(text, text_rect)

    text = font.render("Camera: " + str(simVars["cameraCoords"]), True, simVars["color_overlay_txt"])
    text_rect = text.get_rect(center=(overlay_w/2, 2*overlay_h/3))
    hud.blit(text, text_rect)


    screen.blit(hud, simVars["overlay_pos"])

