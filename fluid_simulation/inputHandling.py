import pygame
import fluid_simulation.fluid_calcs as fluid

def handleInputs(simVars):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_j]:
        simVars["gameObjects"][0] = fluid.step_fluid_sim(simVars["gameObjects"][0])