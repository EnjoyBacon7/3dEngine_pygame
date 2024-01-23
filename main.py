import graphics_engine.graphics as graphics
import simulation
import inputHandling

import args
import numpy as np
import pygame

import cProfile
import pstats


def main():

    # Retrieve the initial variables
    render_class, simulation_class, screen = init_sim()

    # Start the simulation loop
    loop_sim(render_class, simulation_class, screen)


def init_sim():
    # Retrieve arguments from the command line
    runtime_arguments = args.init()

    # Initialise pygame and the simulation
    render_class = graphics.Rendering(runtime_arguments)

    simulation_class = simulation.Simulation([addGameObject("cube.obj")])

    screen = initPygame(render_class)

    return render_class, simulation_class, screen


def loop_sim(render_class, simulation_class, screen):

    while True:

        # Handle input and events
        inputHandling.handleInputs(render_class)
        # Display on screen
        render_class.draw(screen, simulation_class)


def addGameObject(fileName):
    objectFile = open("obj_files/" + fileName, "r")

    lines = objectFile.readlines()
    pointLines = list(filter(lambda x: x[0] == "v" and x[1] == " ", lines))
    for i in range(len(pointLines)):
        pointLines[i] = pointLines[i][2:-2].split(" ")
        for j in range(len(pointLines[i])):
            pointLines[i][j] = float(pointLines[i][j])
    points = np.array(pointLines)

    faceLines = list(filter(lambda x: x[0] == "f" and x[1] == " ", lines))
    for i in range(len(faceLines)):
        faceLines[i] = faceLines[i][2:-2].split(" ")
        facePoints = [
            int(faceLines[i][0].split("/")[0]),
            int(faceLines[i][1].split("/")[0]),
            int(faceLines[i][2].split("/")[0]),
        ]
        faceLines[i] = facePoints

    faces = np.array(faceLines)

    object = simulation.GameObject(points, faces)

    objectFile.close()

    return object


def initPygame(render_class):
    pygame.init()
    screen = pygame.display.set_mode(render_class.resolution, pygame.RESIZABLE)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.display.set_caption("3dEngine Pygame")
    return screen


if __name__ == "__main__":
    cProfile.run('main()', 'profile.out')

    p = pstats.Stats('profile.out')
    p.sort_stats('cumulative').print_stats(30)
