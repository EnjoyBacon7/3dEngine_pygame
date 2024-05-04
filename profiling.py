import time
import json
import numpy as np
import matplotlib as mpl

import inputHandling
import graphics_engine.graphics as graphics
import simulation


def start(runtime_arguments, screen):
    """The profiling function.

    Parameters
    ----------
    runtime_arguments : dict
        The runtime arguments
    screen : pygame.Surface
        The pygame screen
    """

    max_particles = 200

    # Initialise pygame and the simulation
    render_class = graphics.Rendering(screen, runtime_arguments)
    render_class.camera["position"] = np.array([0.78, 1.1, -2.26])

    simulation_class = simulation.Simulation(gameObjects=[],
                                             fluids=[simulation.addFluid(max_particles, [0, 0, 0], [2, 2, 2])])

    profile_data = {
        "update": [],
    }
    for i in range(max_particles):
        profile_data["update"].append([])

    for i in range(max_particles):
        dt = 0.00001
        count = 0

        simulation_class.fluids[0].particles.pop()

        while count < 100:

            frame_start = time.time()

            input_time = time.time()
            # Handle input and events
            inputHandling.handleInputs(render_class)

            display_time = time.time()
            # Display on screen
            render_class.draw(simulation_class)

            update_time = time.time()
            # Update the simulation
            for fluid in simulation_class.fluids:
                fluid.update(dt)

            dt = time.time() - frame_start

            frame_end = time.time()

            profile_data["update"][max_particles - i - 1].append(frame_end - update_time)

            count += 1

        print(f"Finished {max_particles - i} particles")

    formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    with open(f"./profiles/profile_data_{formatted_time}.json", "w") as f:
        json.dump(profile_data, f)

    print("Finished profiling")

    graph_profile(profile_data)


def graph_profile(profile_data):
    """Graphs the profiling data."""

    import matplotlib.pyplot as plt

    plt.figure(figsize=(20, 10))
    plt.title("Update time vs number of particles")
    plt.xlabel("Number of particles")
    plt.ylabel("Update time (ms)")

    for i in range(len(profile_data["update"])):
        plt.scatter([i + 1] * len(profile_data["update"][i]), [x * 1000 for x in profile_data["update"][i]], s=1)

    # display average time for each number of particles as text
    average_times = []
    for i in range(len(profile_data["update"])):
        average_times.append(np.average(profile_data["update"][i]) * 1000)

    plt.savefig("./profiles/profile_graph.png")

    plt.show()