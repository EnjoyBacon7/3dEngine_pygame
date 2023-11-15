import pygame
import fluid_simulation.fluid_calcs as fluid
import multiprocessing

def handleSimulation(simVars, pipes):
    while simVars["running"]:
        # Get the updated simVars from the display process
        if pipes[0][0].poll():
            simVars = pipes[0][0].recv()
        if simVars["step_sim"] == True:
            simVars["gameFluids"][0] = fluid.step_fluid_sim(simVars["gameFluids"][0])
            simVars["step_sim"] = False
            # Send the updated simVars back to the display process
            pipes[1][1].send(simVars)