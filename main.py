import pygame
import simulation_py.config as config
import simulation_py.simulation as simulation
import args
import numpy as np

import cProfile
import pstats

def main():

    # Retrieve arguments from the command line
    runtime_arguments = args.init()

    # Initialise pygame and the simulation
    screen = initPygame(runtime_arguments)
    simVars = simulation.init(runtime_arguments)

    # Define some initial Points
    cube = loadGameObjectObj("my_cube.obj")

    simVars["gameObjects"].append(cube)

    # Start the simulation
    simulation.loop(simVars, screen)


def initPygame(args):
    pygame.init()
    screen = pygame.display.set_mode(args.resolution, pygame.RESIZABLE)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.display.set_caption("3dEngine Pygame")
    return screen

def loadGameObjectObj(fileName):
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
    object = {
        "points": points,
        "faces": faces
    }

    objectFile.close()

    return object

if __name__ == "__main__":
    main()
