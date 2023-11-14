import pygame
import graphics_engine.config as config
import graphics_engine.simulation as simulation
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
    fluidBody = addFluidBody(1, np.array([0, 0, 0]), 100)

    #simVars["gameObjects"].append(cube)
    simVars["gameObjects"].append(fluidBody)

    # Start the simulation
    simulation.loop(simVars, screen)


def initPygame(args):
    pygame.init()
    screen = pygame.display.set_mode(args.resolution, pygame.RESIZABLE)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.display.set_caption("3dEngine Pygame")
    return screen

def addFluidBody(concentration, position, nb_molecules):
    # Create a fluid body
    bodyDim = nb_molecules**(1/3)

    points = []
    velocities = []

    for i in range(nb_molecules):
        # Create a molecule
        points.append(np.array([(position[0] + (i % bodyDim))/concentration, (position[1] + ((i // bodyDim) % bodyDim))/concentration, (position[2] + (i // (bodyDim**2)))/concentration]))
        velocities.append(np.array([0, 0, 0]))
    
    # Add the molecules to the fluid body
    fluidBody = {
        "points": np.array(points, dtype=float),
        "velocities": np.array(velocities, dtype=float),

        "faces": np.array([]) # Not used
    }

    return fluidBody

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
    cProfile.run('main()', 'profile.out')

    p = pstats.Stats('profile.out')
    p.sort_stats('cumulative').print_stats(30)
