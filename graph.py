import matplotlib.pyplot as plt
from datetime import datetime

def plot_log(log):
    
    fig = plt.figure()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%d-%m-%Y %H:%M:%S")
    fig_title = "Frame time graph - " + formatted_time

    graph_plot = fig.add_subplot(211)

    graph_plot.plot(log["points"]["render_time"], label="points frametime")
    graph_plot.plot(log["wireframe"]["render_time"], label="wireframe frametime")
    graph_plot.plot(log["solid"]["render_time"], label="solid frametime")

    graph_plot.set_xlabel("Frame")
    graph_plot.set_ylabel("Time (ms)")

    graph_plot.legend()
    graph_plot.title.set_text("Frame time")

    info_plots = [fig.add_subplot(234), fig.add_subplot(235), fig.add_subplot(236)]
    plot_types = ["points", "wireframe", "solid"]

    for i in range(len(info_plots)):

        # Hide the ticks
        info_plots[i].tick_params(axis='both', which='both', length=0, labelbottom=False, labelleft=False)

        # Add a border
        for spine in info_plots[i].spines.values():
            spine.set_linewidth(0.75)
            spine.set_color('black')

        plot_pos = info_plots[i].get_position().bounds
        new_pos = [plot_pos[0], plot_pos[1], plot_pos[2], plot_pos[3] - 0.05]
        info_plots[i].set_position(new_pos)
        info_plots[i].text(0.5, 0.9, plot_types[i].capitalize() + " render", ha='center', va='center', size=11)
        info_plots[i].text(0.1, 0.7, "Points: " + str(log[plot_types[i]]["rendered_points"]))
        info_plots[i].text(0.1, 0.6, "Faces: " + str(log[plot_types[i]]["rendered_faces"]))

    plt.suptitle(fig_title, fontsize=16)
    plt.savefig("graphs/" + formatted_time + ".svg")
    plt.show()