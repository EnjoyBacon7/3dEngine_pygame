import graphics_engine.graphics as graphics
import simulation
import inputHandling
import profiling

import args
import numpy as np
import pygame

import cProfile
import pstats
import time


def main():
    """The entry point of the program. It initialises the simulation and starts the simulation loop.
    """

    # Retrieve the initial variables
    render_class, simulation_class, runtime_arguments, screen = init_sim()

    # Start the simulation loop
    if runtime_arguments.profile_run == False:
        loop_sim(render_class, simulation_class, screen)
    else:
        profiling.start(runtime_arguments, screen)


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

    screen = initPygame(runtime_arguments.resolution)

    # Initialise the render engine and the simulation
    render_class = graphics.Rendering(screen, runtime_arguments)

    simulation_class = simulation.Simulation(gameObjects=[],
                                             fluids=[simulation.addFluid(800, [0, 0, 0], [5, 10, 5])])

    return render_class, simulation_class, runtime_arguments, screen


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

    # Initialize dt with an arbitrary small value
    dt = 0.00001
    while True:

        frame_start = time.time()

        # Handle input and events
        inputHandling.handleInputs(render_class)
        # Display on screen
        render_class.draw(simulation_class)

        # Update the simulation
        for fluid in simulation_class.fluids:
            fluid.update(dt)

        dt = time.time() - frame_start


def initPygame(resolution):
    """Initialises pygame and returns the screen.

    Parameters
    ----------
    render_class : graphics.Rendering
        The rendering class

    Returns
    -------
    resolution : pygame.Surface
        The resolution of the screen
    """

    pygame.init()
    screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.display.set_caption("3dEngine Pygame")
    return screen


if __name__ == "__main__":

    main()


    # cProfile.run('main()', 'profile.out')

    # p = pstats.Stats('profile.out')
    # p.sort_stats('cumulative').print_stats(30)
