import pygame
import time
import graph

import cProfile
import numpy as np

import graphics_engine.config as config
import graphics_engine.utilities as utilities
import graphics_engine.inputHandling as inputHandling
import graphics_engine.display as display

# ----------------------------------------
# Initialise the simulation
# ----------------------------------------


def init(args):
    simVars = {
        # World composition
        "gameObjects": [],

        # Camera variables
        "cameraCoords": np.array([0, 0, -20], dtype=float),
        "cameraRot": np.array([0, 0, 0], dtype=float),
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