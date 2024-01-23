import numpy as np
import uuid


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

        for particle in self.particles:
            particle.velocity += self.calculateParticleAcceleration(particle.id, dt)
            particle.position += particle.velocity

            # Check for collisions with the bounds
            if particle.position[0] < self.bounds[0]:
                particle.position[0] = self.bounds[0]
                particle.velocity[0] = 0
            elif particle.position[0] > self.bounds[3]:
                particle.position[0] = self.bounds[3]
                particle.velocity[0] = 0
            if particle.position[1] < self.bounds[1]:
                particle.position[1] = self.bounds[1]
                particle.velocity[1] = 0
            elif particle.position[1] > self.bounds[4]:
                particle.position[1] = self.bounds[4]
                particle.velocity[1] = 0
            if particle.position[2] < self.bounds[2]:
                particle.position[2] = self.bounds[2]
                particle.velocity[2] = 0
            elif particle.position[2] > self.bounds[5]:
                particle.position[2] = self.bounds[5]
                particle.velocity[2] = 0

    def calculateParticleAcceleration(self, particleId, dt):
        """Calculates the acceleration of a particle

        Parameters
        ----------
        particleId : uuid.UUID
            The id of the particle
        dt : float
            The time step

        Returns
        -------
        acceleration : np.array
            The acceleration of the particle
        """

        acceleration = np.zeros(3)

        for particle in self.particles:
            # Calculate particle interactions
            if particle.id != particleId:
                acceleration += self.calculateParticleInteraction(
                    particleId, particle.id, dt)
            # Add gravity
            acceleration += np.array([0, -9.81, 0]) / particle.mass * dt

        return acceleration

    def calculateParticleInteraction(self, particleId1, particleId2, dt):
        """Calculates the acceleration between two particles

        Parameters
        ----------
        particleId1 : uuid.UUID
            The id of the first particle
        particleId2 : uuid.UUID
            The id of the second particle
        dt : float
            The time step

        Returns
        -------
        acceleration : np.array
            The acceleration between the two particles
        """

        acceleration = np.zeros(3)

        particle1 = self.getParticleById(particleId1)
        particle2 = self.getParticleById(particleId2)

        if particle1 is None or particle2 is None:
            print("Particle not found")
            return acceleration

        # Calculate the distance between the two particles
        distance = np.sqrt(
            (particle1.position[0] - particle2.position[0])**2 +
            (particle1.position[1] - particle2.position[1])**2 +
            (particle1.position[2] - particle2.position[2])**2
        )

        # Calculate the force between the two particles
        force = 10 * (distance - 1)

        # Calculate the direction of the force
        direction = np.array([
            particle1.position[0] - particle2.position[0],
            particle1.position[1] - particle2.position[1],
            particle1.position[2] - particle2.position[2]
        ])

        # Normalize the direction
        length = np.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)
        direction /= length

        # Calculate the acceleration
        acceleration = direction * force / particle1.mass * dt

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
        particles.append(Particle(np.random.rand(3) * 10, np.zeros(3)))

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
