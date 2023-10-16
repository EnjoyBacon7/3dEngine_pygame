import pygame
import config
import simulation

def main():

    # Initialise pygame and the simulation
    screen = initPygame()
    simVars = simulation.init()

    # Define some initial Points
    loadObj(simVars, "hmm.obj")

    # Start the simulation
    simulation.loop(simVars, screen)


def initPygame():
    pygame.init()
    screen = pygame.display.set_mode(config.RESOLUTION, pygame.RESIZABLE)
    pygame.display.set_caption("3dEngine")
    return screen

def loadObj(simVars, fileName):
    object = open("obj files/" + fileName, "r")
    lines = object.readlines()
    lines = list(filter(lambda x: x[0] == "v", lines))
    for i in range(len(lines)):
        lines[i] = lines[i][2:-2].split(" ")
        for j in range(len(lines[i])):
            lines[i][j] = float(lines[i][j])
    points = lines

    simVars["points"] = points
    
    


if __name__ == "__main__":
    main()