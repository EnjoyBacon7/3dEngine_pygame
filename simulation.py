import numpy as np
import uuid
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
    bounds : np.array
        An array of the bounds of the fluid
    """

    def __init__(self, particles, bounds):
        self.particles = particles
        self.bounds = bounds

    def update(self, dt):
        """Updates the fluid by calculating each particle's acceleration and moving the particles according to their velocity

        Parameters
        ----------
        dt : float
            The time step
        """

        accelerations = self.calculateParticleAccelerations(dt)

        for particle in self.particles:
            particle.velocity += accelerations[self.particles.index(particle)]
            particle.position += particle.velocity

            # Check for collisions with the bounds

            if particle.position[0] < self.bounds[0]:
                particle.position[0] = self.bounds[0]
                particle.velocity[0] = - (particle.velocity[0] * 0.5)
            elif particle.position[0] > self.bounds[3]:
                particle.position[0] = self.bounds[3]
                particle.velocity[0] = - (particle.velocity[0] * 0.5)
            if particle.position[1] < self.bounds[1]:
                particle.position[1] = self.bounds[1]
                particle.velocity[1] = - (particle.velocity[1] * 0.5)
            elif particle.position[1] > self.bounds[4]:
                particle.position[1] = self.bounds[4]
                particle.velocity[1] = - (particle.velocity[1] * 0.5)
            if particle.position[2] < self.bounds[2]:
                particle.position[2] = self.bounds[2]
                particle.velocity[2] = - (particle.velocity[2] * 0.5)
            elif particle.position[2] > self.bounds[5]:
                particle.position[2] = self.bounds[5]
                particle.velocity[2] = - (particle.velocity[2] * 0.5)

    def calculateParticleAccelerations(self, dt):
        """Calculates the accelerations of all particles

        Parameters
        ----------
        particle: Particle
            The particle
        dt : float
            The time step

        Returns
        -------
        acceleration : np.array
            The acceleration of the particle
        """
        accelerations = np.zeros((len(self.particles), 3))
        interactions_list = set()
        for i in range(len(self.particles)):
            currentParticle = self.particles[i]
            for j in range(len(self.particles)):
                otherParticle = self.particles[j]
                if i != j and (j, i) not in interactions_list:
                    interaction_acceleration = self.calculateParticleInteraction(
                        currentParticle, otherParticle, dt)
                    accelerations[i] += interaction_acceleration
                    accelerations[j] -= interaction_acceleration
                    interactions_list.add((i, j))
        return accelerations

    def calculateParticleInteraction(self, particle1, particle2, dt):
        """Calculates the acceleration between two particles

        Parameters
        ----------
        particle1 : Particle
            The first particle
        particle2 : Particle
            The second particle
        dt : float
            The time step

        Returns
        -------
        acceleration : np.array
            The acceleration between the two particles
        """

        start = time.time()

        acceleration = np.zeros(3)

        if particle1 is None or particle2 is None:
            print("Particle not found")
            return acceleration

        if particle1.position[0] == particle2.position[0] and particle1.position[1] == particle2.position[1] and particle1.position[2] == particle2.position[2]:
            print("Particles are in the same position")
            particle1.position[0] += np.random.rand() * 0.01
            particle1.position[1] += np.random.rand() * 0.01
            particle1.position[2] += np.random.rand() * 0.01

        # Calculate the vector between the two particles
        vector = np.array([
            particle1.position[0] - particle2.position[0],
            particle1.position[1] - particle2.position[1],
            particle1.position[2] - particle2.position[2]
        ])

        # Calculate the distance between the two particles
        distance = abs(vector[0]) + abs(vector[1]) + abs(vector[2])

        # Calculate the force between the two particles
        force = (0.05/(2*distance)) - (0.025)
        if force < 0:
            return acceleration
        if force > 0.5:
            force = 0.5

        vector /= distance

        # Calculate the acceleration /// ONLY WORKS FOR PARTICLES OF EQUAL MASS
        multiplier = force / particle1.mass * dt
        acceleration = vector * multiplier

        return acceleration

    def getParticleById(self, particleId):
        """Returns the particle with the given id

        Parameters
        ----------
        particleId : uuid.UUID
            The id of the particle

        Returns
        -------
        particle : Particle
            The particle with the given id
        """

        for particle in self.particles:
            if particle.id == particleId:
                return particle

        return None


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
        self.id = uuid.uuid4()
        self.position = position
        self.velocity = velocity
        self.mass = mass


def addFluid(nb_particles, bounds=[0, 0, 0, 10, 10, 10]):
    """Adds a fluid to the simulation.

    Parameters
    ----------
    nb_particles : int
        The number of particles in the fluid
    bounds : np.array
        The bounds of the fluid

    Returns
    -------
    fluid : simulation.Fluid
        The fluid
    """

    particles = []
    for i in range(nb_particles):
        position = np.array([
            np.random.rand() * (bounds[3] - bounds[0]) + bounds[0],
            np.random.rand() * (bounds[4] - bounds[1]) + bounds[1],
            np.random.rand() * (bounds[5] - bounds[2]) + bounds[2]
        ])
        velocity = np.zeros(3)
        particles.append(Particle(position, velocity))

    fluid = Fluid(particles, bounds)

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
