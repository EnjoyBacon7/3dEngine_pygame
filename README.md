# 3dEngine_pygame
 A pygame implementation of a simple 3d Engine

https://github.com/user-attachments/assets/5c1256b0-fe40-4b3c-8bd2-861ccba4842f

## Setup

It is recommended to create a virtual environment to avoid clashing versions of dependencies, however it is not critical.

Install required python packages with the following command:

```
pip3 install -r requirements.txt
```

You can then simply run the program with the following command

```
python3 main.py
```

If your hardware does not allow for reasonable performance with the default settings, you are welcome to change the number of simulated particles in `main.py`at the following line

```
simulation_class = simulation.Simulation(gameObjects=[], fluids=[simulation.addFluid(800, [0, 0, 0], [5, 10, 5])])
```

(800 is the number you are looking to change)

## Arguments

- `--resolution` `-r` : Set the resolution of the window
- `--overlay` `-o` : Enable the overlay of the debug pane
- `--render-mode` `-rm` : Set the render mode of the engine
- `--fps` `-fps` : Set the fps of the engine (unused currently as multiprocessing is a nightmare)
- `--profile-run` `-p` : Profile the run of the engine
