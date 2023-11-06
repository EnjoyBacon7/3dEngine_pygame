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
    pointLines = list(filter(lambda x: x[0] == "v" and x[1] == " ", lines))
    for i in range(len(pointLines)):
        pointLines[i] = pointLines[i][2:-2].split(" ")
        for j in range(len(pointLines[i])):
            pointLines[i][j] = float(pointLines[i][j])
    points = pointLines

    faceLines = list(filter(lambda x: x[0] == "f" and x[1] == " ", lines))
    for i in range(len(faceLines)):
        faceLines[i] = faceLines[i][2:-2].split(" ")
        facePoints = [
            int(faceLines[i][0].split("/")[0]),
            int(faceLines[i][1].split("/")[0]),
            int(faceLines[i][2].split("/")[0]),
        ]
        faceLines[i] = facePoints

    faces = faceLines
    object = {
        "points": points,
        "faces": faces
    }

    objectFile.close()

    return object

if __name__ == "__main__":
    main()