import pygame
import config

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

        # Other variables
        "screenResolution": config.RESOLUTION,
        "clock": pygame.time.Clock(),
        "hideOverlay": False,
    }
    return simVars

def loop(simVars, screen):

    running = True
    while running:

        # Handle input and events
        handleEvents(simVars)
        # Display on screen
        handleDisplay(simVars, screen)
        # Limit fps
        simVars["clock"].tick(60)

def handleEvents(simVars):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.VIDEORESIZE:
                simVars["screenResolution"] = event.size
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    simVars["hideOverlay"] = not simVars["hideOverlay"]

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

def handleDisplay(simVars, screen):

    camera = simVars["cameraCoords"]
    canvasPoints = []

    # Clear the screen
    screen.fill((0,0,0))

    # Math out the 3d points on the canvas (1 unit away from the camera)
    for i in range(len(simVars["points"])):
        point = simVars["points"][i]
        resolution = simVars["screenResolution"]
        ratio = resolution[0]/resolution[1]
        # Rounding isn't great
        coords = [(point[0] - camera[0])/(point[2] - camera[2]) * ratio * 300 + resolution[0]/2, (point[1] - camera[1])/(-(point[2] - camera[2])) * ratio * 300 + resolution[1]/2]
        canvasPoints.append(coords)
    
    # Draw the points
    for point in canvasPoints:
        pygame.draw.circle(screen, (255, 255, 255), point, 3)

    # Draw the overlay
    if(not simVars["hideOverlay"]):
        drawOverlay(simVars, screen)

    # Apply changes to screen
    pygame.display.flip()

def drawOverlay(simVars, screen):
    font = pygame.font.SysFont("Roboto", 30)
    points = simVars["points"]

    overlay_w = config.OVERLAY_SIZE[0]
    overlay_h = config.OVERLAY_SIZE[1]

    hud = pygame.Surface((overlay_w, overlay_h), pygame.SRCALPHA)

    pygame.draw.rect(hud, config.COLOR_OVERLAY_BG, (0, 0, overlay_w, overlay_h), 0, 10)
    pygame.draw.rect(hud, config.COLOR_OVERLAY_BORDER, (0, 0, overlay_w, overlay_h), 2, 10)

    text = font.render("Points: " + str(points), True, config.COLOR_OVERLAY_TXT)
    text_rect = text.get_rect(center=(overlay_w/2, overlay_h/3))
    hud.blit(text, text_rect)

    text = font.render("Camera: " + str(simVars["cameraCoords"]), True, config.COLOR_OVERLAY_TXT)
    text_rect = text.get_rect(center=(overlay_w/2, 2*overlay_h/3))
    hud.blit(text, text_rect)

    screen.blit(hud, config.OVERLAY_POS)