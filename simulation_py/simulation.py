import pygame
import time
import graph

import cProfile

import simulation_py.config as config
import simulation_py.utilities as utilities
import simulation_py.inputHandling as inputHandling
import simulation_py.display as display

# ----------------------------------------
# Initialise the simulation
# ----------------------------------------


def init(args):
    simVars = {
        # World composition
        "gameObjects": [],

        # Camera variables
        "cameraCoords": [0, 0, -5],
        
        "cameraRot": [0, 0, 0],
        "fov": 90,
        "farClip": 100,
        "nearClip": 0.1,
        "projection_matrix": [],

        # Loading variables from config.py
        "resolution": args.resolution,
        "overlay_size": (config.OVERLAY_SIZE[0]/100 * config.RESOLUTION[0], config.OVERLAY_SIZE[1]/100 * config.RESOLUTION[1]),
        "overlay_pos": (config.OVERLAY_POS[0]/100 * config.RESOLUTION[0], config.OVERLAY_POS[1]/100 * config.RESOLUTION[1]),
        "color_overlay_bg": config.COLOR_OVERLAY_BG,
        "color_overlay_border": config.COLOR_OVERLAY_BORDER,
        "color_overlay_txt": config.COLOR_OVERLAY_TXT,
        "color_points": config.COLOR_POINTS,
        "show_overlay": args.overlay,

        # Rendering variables
        # "wireframe", "solid", or "points"
        "render_mode": "points" if args.log == True else args.render_mode,

        "running": True,
        "display_timestamp": 0,
        "input_timestamp": 0,

        # Logging variables
        "start_timestamp": time.time(),
        "frame_nb": 0,
        "enable_logging": args.log,
        "log": {
            "input_handler_time": [],
            "resolution": args.resolution,
            "target_fps": args.fps,
            "points": {
                "rendered_points": 0,
                "rendered_faces": 0,
                "render_time": [],
                "test_time": 0,
            },
            "wireframe": {
                "rendered_points": 0,
                "rendered_faces": 0,
                "render_time": [],
                "test_time": 0,
            },
            "solid": {
                "rendered_points": 0,
                "rendered_faces": 0,
                "render_time": [],
                "test_time": 0,
            },
        }
    }

    simVars["projection_matrix"] = utilities.getProjectionMatrix(simVars)

    return simVars

# ----------------------------------------
# Main loop
# ----------------------------------------


def loop(simVars, screen):

    while simVars["running"]:

        # Handle input and events
        inputHandling.handleInputs(simVars)
        # Display on screen
        display.handleDisplay(simVars, screen)

    pygame.quit()
    if simVars["enable_logging"]:
        graph.plot_log(simVars["log"])