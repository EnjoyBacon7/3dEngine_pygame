import graphics_engine.graphics as graphics
import simulation
import inputHandling

import args
import numpy as np
import pygame

import cProfile
import pstats


def main():
    """The main function of the program. It initialises the simulation and starts the simulation loop.
    """

    # Retrieve the initial variables
    render_class, simulation_class, screen = init_sim()

    # Start the simulation loop
    loop_sim(render_class, simulation_class, screen)


def init_sim():
    """Initialises the simulation and returns the initial variables.

    Returns
    -------
    render_class : graphics.Rendering
        The rendering class
    simulation_class : simulation.Simulation
        The simulation class
    screen : pygame.Surface
        The pygame screen
    """

    # Retrieve arguments from the command line
    runtime_arguments = args.init()

    # Initialise pygame and the simulation
    render_class = graphics.Rendering(runtime_arguments)

    simulation_class = simulation.Simulation(gameObjects=[simulation.addGameObject("cube.obj")],
                                             fluids=[simulation.addFluid(20)])

    screen = initPygame(render_class)

    return render_class, simulation_class, screen


def loop_sim(render_class, simulation_class, screen):
    """The simulation loop. This is where the simulation is updated and rendered.

    Parameters
    ----------
    render_class : graphics.Rendering
        The rendering class responsible for rendering the simulation
    simulation_class : simulation.Simulation
        The simulation class responsible for updating the simulation
    screen : pygame.Surface
        The pygame screen on which the simulation is rendered
    """
    while True:
        # Handle input and events
        inputHandling.handleInputs(render_class)
        # Display on screen
        render_class.draw(screen, simulation_class)

        # Update the simulation
        for fluid in simulation_class.fluids:
            fluid.update(0.1)


def initPygame(render_class):
    """Initialises pygame and returns the screen.

    Parameters
    ----------
    render_class : graphics.Rendering
        The rendering class

    Returns
    -------
    screen : pygame.Surface
        The pygame screen
    """

    pygame.init()
    screen = pygame.display.set_mode(render_class.resolution, pygame.RESIZABLE)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.display.set_caption("3dEngine Pygame")
    return screen


if __name__ == "__main__":
    cProfile.run('main()', 'profile.out')

    p = pstats.Stats('profile.out')
    p.sort_stats('cumulative').print_stats(30)
