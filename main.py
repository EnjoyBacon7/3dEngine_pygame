import pygame
import config
import simulation

def main():

    # Initialise pygame and the simulation
    screen = initPygame()
    simVars = simulation.init()

    # Define some initial Points
    cube = loadGameObjectObj("my_cube.obj")

    simVars["gameObjects"].append(cube)

    # Start the simulation
    simulation.loop(simVars, screen)


def initPygame():
    pygame.init()
    screen = pygame.display.set_mode(config.RESOLUTION, pygame.RESIZABLE)
    pygame.display.set_caption("3dEngine Pygame")
    return screen

def loadGameObjectObj(fileName):
    objectFile = open("obj_files/" + fileName, "r")
    lines = objectFile.readlines()
    lines = list(filter(lambda x: x[0] == "v" and x[1] == " ", lines))
    for i in range(len(lines)):
        lines[i] = lines[i][2:-2].split(" ")
        for j in range(len(lines[i])):
            lines[i][j] = float(lines[i][j])
    points = lines
    print(points)

    object = {
        "points": points
    }

    objectFile.close()

    return object

if __name__ == "__main__":
    main()