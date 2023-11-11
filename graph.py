import matplotlib.pyplot as plt
from datetime import datetime
import json

def plot_log(log):
    
    fig = plt.figure()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%d-%m-%Y %H:%M:%S")
    fig_title = "Frame time graph - " + formatted_time

    graph_plot = fig.add_subplot(211)

    sec_to_ms = lambda x: x * 1000
    points_ms = list(map(sec_to_ms, log["points"]["render_time"]))
    wireframe_ms = list(map(sec_to_ms, log["wireframe"]["render_time"]))
    solid_ms = list(map(sec_to_ms, log["solid"]["render_time"]))

    graph_plot.plot(points_ms, label="points frametime")
    graph_plot.plot(wireframe_ms, label="wireframe frametime")
    graph_plot.plot(solid_ms, label="solid frametime")

    graph_plot.set_xlabel("Frame")
    graph_plot.set_ylabel("Time (ms)")

    graph_plot.legend()
    graph_plot.title.set_text("Frame time")

    info_plots = [fig.add_subplot(245), fig.add_subplot(246), fig.add_subplot(247)]
    general_plot = fig.add_subplot(248)
    plot_types = ["points", "wireframe", "solid"]

    for i in range(len(info_plots)):

        # Hide the ticks
        info_plots[i].tick_params(axis='both', which='both', length=0, labelbottom=False, labelleft=False)

        # Add a border
        for spine in info_plots[i].spines.values():
            spine.set_linewidth(0.75)
            spine.set_color('black')

        avg_fps = round(1 / (sum(log[plot_types[i]]["render_time"]) / len(log[plot_types[i]]["render_time"])), 2)

        plot_pos = info_plots[i].get_position().bounds
        new_pos = [plot_pos[0], plot_pos[1], plot_pos[2], plot_pos[3] - 0.05]
        info_plots[i].set_position(new_pos)
        info_plots[i].text(0.5, 0.9, plot_types[i].capitalize() + " render", ha='center', va='center', size=11)
        info_plots[i].text(0.1, 0.7, "Vertices: " + str(log[plot_types[i]]["rendered_points"]))
        info_plots[i].text(0.1, 0.6, "Faces: " + str(log[plot_types[i]]["rendered_faces"]))
        info_plots[i].text(0.1, 0.5, "Resolution: " + str(log["resolution"][0]) + "x" + str(log["resolution"][1]))
        info_plots[i].text(0.1, 0.4, "Avg FPS: " + str(avg_fps))
        info_plots[i].text(0.1, 0.3, "(Assuming render only)")
        info_plots[i].text(0.1, 0.2, "Test time: " + str(round(log[plot_types[i]]["test_time"], 3)) + "s")

    general_plot.tick_params(axis='both', which='both', length=0, labelbottom=False, labelleft=False)
    general_plot_pos = general_plot.get_position().bounds
    new_pos = [general_plot_pos[0], general_plot_pos[1], general_plot_pos[2], general_plot_pos[3] - 0.05]
    general_plot.set_position(new_pos)
    general_plot.text(0.5, 0.9, "General info", ha='center', va='center', size=11)
    input_time_avg = round((sum(log["input_handler_time"]) / len(log["input_handler_time"]) * 1000), 2)
    general_plot.text(0.1, 0.7, "Input time: " + str(input_time_avg) + "ms")

    plt.suptitle(fig_title, fontsize=16)
    plt.savefig("graphs/" + formatted_time + ".svg")

    f = open("graphs/" + formatted_time + ".json", "w")
    f.write(json.dumps(log))

    plt.show()