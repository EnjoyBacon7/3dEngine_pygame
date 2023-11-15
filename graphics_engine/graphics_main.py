import pygame
import time
import graph

import cProfile
import numpy as np
import multiprocessing
import sys

import graphics_engine.config as config
import graphics_engine.utilities as utilities
import inputHandling as inputHandling
import graphics_engine.rendering as rendering
import pickle

# ----------------------------------------
# Initialise the simulation
# ----------------------------------------


def init(args):
    simVars = {
        # World composition
        "gameObjects": [],
        "gameFluids": [],

        "step_sim": False,

        # Camera variables
        "cameraCoords": np.array([-3.42, 8.2, -5.96], dtype=float),
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
# Main graphics loop
# ----------------------------------------

def initPygame(args):
    pygame.init()
    screen = pygame.display.set_mode(args.resolution, pygame.RESIZABLE)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.display.set_caption("3dEngine Pygame")
    return screen

def loop(simVars, runtime_arguments, pipes):

    screen = initPygame(runtime_arguments)

    while simVars["running"]:

        # Get the updated simVars from the corresponding pipe
        if pipes[1][0].poll():
            simVars = pipes[1][0].recv()

        # Handle input and events
        inputHandling.handleInputs(simVars)
        # Display on screen
        rendering.handleDisplay(simVars, screen)

        # Send the updated simVars to the simulation process
        if not pipes[0][0].poll():
            pipes[0][1].send(simVars)

    pygame.quit()
    if simVars["enable_logging"]:
        graph.plot_log(simVars["log"])