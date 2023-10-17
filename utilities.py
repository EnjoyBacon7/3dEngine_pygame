import pygame
import config

def updateVarsOnResize(simVars):
    print("resize")
    simVars["resolution"] = pygame.display.get_surface().get_size()
    simVars["overlay_size"] = (config.OVERLAY_SIZE[0]/100 * simVars["resolution"][0], config.OVERLAY_SIZE[1]/100 * simVars["resolution"][1])
    simVars["overlay_pos"] = (config.OVERLAY_POS[0]/100 * simVars["resolution"][0], config.OVERLAY_POS[1]/100 * simVars["resolution"][1])