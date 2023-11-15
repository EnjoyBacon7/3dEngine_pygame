import pygame
import graphics_engine.config as config
import graphics_engine.graphics_main as graphics_main
import fluid_simulation.inputHandling as fluid
import args
import numpy as np
import time

import multiprocessing

import cProfile
import pstats

def main():

    # Retrieve arguments from the command line
    runtime_arguments = args.init()

    # Initialise pygame and the simulation
    render_vars = graphics_main.init(runtime_arguments)

    # Define some initial Points
    fluidBody, boundingBox = addFluidBody(200)

    render_vars["gameFluids"].append(fluidBody)
    render_vars["gameObjects"].append(boundingBox)

    # First pipe from display to simulation
    # Second pipe from simulation to display
    pipes = [multiprocessing.Pipe(duplex=False) for i in range(2)]

    renderProcess = multiprocessing.Process(target=graphics_main.loop, args=(render_vars, runtime_arguments, pipes))
    fluidProcess = multiprocessing.Process(target=fluid.handleSimulation, args=(render_vars, pipes))

    renderProcess.start()
    fluidProcess.start()

    renderProcess.join()

def addFluidBody(nb_molecules, bounds=[0, 0, 0, 10, 10, 10]):
    # Create a fluid body
    bodyDim = nb_molecules**(1/3)

    points = []
    velocities = []

    for i in range(nb_molecules):
        # Create a molecule
        x = i % bounds[3] + bounds[0]
        y = (i // bounds[3]) % bounds[4] + bounds[1] + np.random.rand() * 0.1
        z = (i // (bounds[3] * bounds[4])) % bounds[5] + bounds[2] + np.random.rand() * 0.1
        points.append(np.array([x, y, z]))
        velocities.append(np.array([0, 0, 0]))
    
    # Add the molecules to the fluid body
    fluidBody = {
        "points": np.array(points, dtype=float),
        "velocities": np.array(velocities, dtype=float),
    }

    boundingBox = {
        "points": np.array([
            [bounds[0], bounds[1], bounds[2]],
            [bounds[0], bounds[1], bounds[5]],
            [bounds[0], bounds[4], bounds[2]],
            [bounds[0], bounds[4], bounds[5]],
            [bounds[3], bounds[1], bounds[2]],
            [bounds[3], bounds[1], bounds[5]],
            [bounds[3], bounds[4], bounds[2]],
            [bounds[3], bounds[4], bounds[5]],
        ], dtype=float),
        "faces": np.array([
            [1, 2, 1],
            [1, 3, 1],
            [1, 5, 1],
            [2, 4, 2],
            [2, 6, 2],
            [3, 4, 3],
            [3, 7, 3],
            [4, 8, 4],
            [5, 6, 5],
            [5, 7, 5],
            [6, 8, 6],
            [7, 8, 7],

        ], dtype=int)
    }

    return fluidBody, boundingBox

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
