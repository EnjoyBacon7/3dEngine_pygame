import numpy as np
import time


class Simulation:
    """A simulation is a collection of GameObjects and Fluids

    Parameters
    ----------
    gameObjects : list
        A list of GameObjects
    """

    def __init__(self, gameObjects=[], fluids=[]):
        self.gameObjects = gameObjects
        self.fluids = fluids


class GameObject:
    """A game object is a collection of points and faces

    Parameters
    ----------
    points : np.array
        An array of points
    faces : np.array
        An array of faces (the indices of the points that make up the face)
    """

    def __init__(self, points, faces):
        self.points = points
        self.faces = faces


class Fluid:
    """A fluid is a collection of particles

    Parameters
    ----------
    particles : list
        A list of particles
    position : np.array
        An array of the position of the origin of the fluid.
    size : np.array
        An array containing size in the x, y, and z directions
    """

    def __init__(self, particles, position, size):
        self.particles = particles
        self.position = position
        self.size = size

    def update(self, dt):
        """Updates the fluid by calculating each particle's acceleration and moving the particles according to their velocity

        Parameters
        ----------
        dt : float
            The time step
        """

        self.applyParticleInteractions(dt)

        for i, particle in enumerate(self.particles):
            particle.position += particle.velocity

            # Check for collisions with the fluid body

            if particle.position[0] < 0:
                particle.position[0] = 0
                particle.velocity[0] = - (particle.velocity[0] * 0.5)
            elif particle.position[0] > self.size[0]:
                particle.position[0] = self.size[0]
                particle.velocity[0] = - (particle.velocity[0] * 0.5)
            if particle.position[1] < 0:
                particle.position[1] = 0
                particle.velocity[1] = - (particle.velocity[1] * 0.5)
            elif particle.position[1] > self.size[1]:
                particle.position[1] = self.size[1]
                particle.velocity[1] = - (particle.velocity[1] * 0.5)
            if particle.position[2] < 0:
                particle.position[2] = 0
                particle.velocity[2] = - (particle.velocity[2] * 0.5)
            elif particle.position[2] > self.size[2]:
                particle.position[2] = self.size[2]
                particle.velocity[2] = - (particle.velocity[2] * 0.5)

    def applyParticleInteractions(self, dt):
        """Calculates and applies the accelerations of all particles

        Parameters
        ----------
        particle: Particle
            The particle
        dt : float
            The time step
        """

        # Precalculate the vectors between the particles
        positions = np.array([particle.position for particle in self.particles], ndmin=2)
        self.vectors = positions[:, np.newaxis, :] - positions[np.newaxis, :, :]

        # Precalculate the distances between the particles into a single value
        self.distances = np.linalg.norm(self.vectors, axis=2)
        self.distances[self.distances == 0] = 1

        interaction_forces = 1/(self.distances *1000000)

        self.vectors /= self.distances[:, :, np.newaxis]

        multiplier = interaction_forces / np.array([particle.mass for particle in self.particles]) * dt

        accelerations = self.vectors * multiplier[:, :, np.newaxis]

        for i, particle in enumerate(self.particles):
            particle.velocity += np.sum(accelerations[i], axis=0)
            particle.velocity[1] -= 0.00001


class Particle:
    """A particle is a point in space with a velocity and a mass

    Parameters
    ----------
    position : np.array
        The position of the particle
    velocity : np.array
        The velocity of the particle
    mass : float
        The mass of the particle
    """

    def __init__(self, position, velocity, mass=1):
        self.position = position
        self.velocity = velocity
        self.mass = mass


def addFluid(nb_particles, position=[0, 0, 0], size=[10, 10, 10]):
    """Adds a fluid to the simulation.

    Parameters
    ----------
    nb_particles : int
        The number of particles in the fluid
    position : np.array
        The origin of the fluid
    size : np.array
        The size of the fluid in x, y, and z coordinates

    Returns
    -------
    fluid : simulation.Fluid
        The fluid
    """

    particles = []
    for i in range(nb_particles):
        particle_position = np.array([
            np.random.rand() * (size[0]),
            np.random.rand() * (size[1]),
            np.random.rand() * (size[2])
        ])
        velocity = np.zeros(3)
        particles.append(Particle(particle_position, velocity))

    fluid = Fluid(particles, position, size)

    return fluid


def addGameObject(fileName):
    """Adds a game object to the simulation.

    Parameters
    ----------
    fileName : str
        The name of the file containing the object

    Returns
    -------
    object : simulation.GameObject
        The game object
    """

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

    object = GameObject(points, faces)

    objectFile.close()

    return object
