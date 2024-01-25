import time
import pygame
import numpy as np

# ----------------------------------------
# Event and input handling
# ----------------------------------------


def handleInputs(render_class):
    """Handles inputs and events

    Parameters
    ----------
    render_class : graphics.Rendering
        The rendering class responsible for rendering the simulation
    """

    step = 0.1

    handleEvents(render_class)
    debugHandler(render_class, step)
    movementHandler(render_class, step)
    rotationHandler(render_class)


def handleEvents(render_class):
    """Handles events pygame events and key presses

    Parameters
    ----------
    render_class : graphics.Rendering
        The rendering class responsible for rendering the simulation
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # A quit event does not warrant a plot. It is a request for immediate termination (When plotting is implemented)
            exit()
        if event.type == pygame.VIDEORESIZE:
            render_class.updateVarsOnResize(render_class)

        # Here we handle key presses (not key holds)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                render_class.show_overlay = not render_class.show_overlay
            if event.key == pygame.K_p:
                render_class.render_mode = "points"
            if event.key == pygame.K_o:
                render_class.render_mode = "wireframe"
            if event.key == pygame.K_i:
                render_class.render_mode = "solid"
            if event.key == pygame.K_EQUALS:
                if pygame.mouse.get_visible():
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                else:
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)


def movementHandler(render_class, step):
    """Handles movement of the camera

    Parameters
    ----------
    render_class : graphics.Rendering
        The rendering class responsible for rendering the simulation
    step : float
        The step size of the movement
    """

    keys = pygame.key.get_pressed()

    # Save calculations by calculating only if needed
    if not (
            keys[pygame.K_s] or keys[pygame.K_z] or keys[pygame.K_q] or
            keys[pygame.K_d] or keys[pygame.K_e] or keys[pygame.K_a]):
        return

    # Calculate camera direction vector
    dir_vec3 = np.array([np.sin(render_class.camera["rotation"][1]), -np.sin(render_class.camera["rotation"]
                        [0]), -np.cos(render_class.camera["rotation"][1])])

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

    # Apply movement
    if keys[pygame.K_s]:
        render_class.camera["position"] += dir_vec3 * step
    if keys[pygame.K_z]:
        render_class.camera["position"] -= dir_vec3 * step
    if keys[pygame.K_q]:
        render_class.camera["position"] -= strafe_vec3 * step
    if keys[pygame.K_d]:
        render_class.camera["position"] += strafe_vec3 * step
    if keys[pygame.K_e]:
        render_class.camera["position"][1] += step
    if keys[pygame.K_a]:
        render_class.camera["position"][1] -= step


def rotationHandler(render_class):
    """Handles rotation of the camera using the mouse

    Parameters
    ----------
    render_class : graphics.Rendering
        The rendering class responsible for rendering the simulation
    """

    mouse_move = pygame.mouse.get_rel()
    render_class.camera["rotation"][0] -= mouse_move[1]/100
    render_class.camera["rotation"][1] -= mouse_move[0]/100


def debugHandler(render_class, step):
    """Handles debug inputs and temporary debug features

    Parameters
    ----------
    render_class : graphics.Rendering
        The rendering class responsible for rendering the simulation
    step : float
        The step size of the movement
    """

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        # Rotate camera on z axis
        if keys[pygame.K_LEFT]:
            render_class.camera["rotation"][2] -= step
        if keys[pygame.K_RIGHT]:
            render_class.camera["rotation"][2] += step
