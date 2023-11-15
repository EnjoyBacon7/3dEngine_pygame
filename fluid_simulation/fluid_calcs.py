import numpy as np

# Here each molecule is compared to every other molecule, which is not efficient, but easy to implement

# molecule = [position_vec3, velocity_vec3]
def step_fluid_sim(molecules):

    accelerations = np.zeros((len(molecules["points"]), 3))

    for i in range(len(molecules["points"])):
        acceleration_vector = get_molecule_interaction(i, molecules["points"][i], molecules["points"])
        acceleration_vector += np.array([0, -9.81 / 10000, 0])
        accelerations[i] = acceleration_vector

    # Apply the accelerations to the molecules' velocities
    molecules["velocities"] += accelerations
    
    # Apply the velocities to the molecules' positions
    molecules["points"] += molecules["velocities"]

    apply_collisions(molecules)

    return molecules

def get_molecule_interaction(index, molecule_pos, molecules_pos):
    acceleration_vector = np.zeros(3)

    for i, temp_molecule_pos in enumerate(molecules_pos):
        # Kinda stupid for two molecules to be in the same place, but it's possible and it won't handle it
        if(i == index):
            continue

        # Get the vector between the main molecule and the temp molecule
        vector = molecule_pos - temp_molecule_pos

        # Get the distance between the two molecules
        distance = np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
        if distance > 1:
            continue

        # If the points are at the same position, offest the temp molecule a bit to avoid division by 0
        elif distance == 0:
            temp_molecule_pos += (np.random.rand(3) - 1) / 100000  
        
        # Normalize the vector
        vector /= distance
        # Apply the force to the main molecule based on the distance
        acceleration_vector += vector / (distance*10)**3 # Displacement vector inversely exponential to distance

    return acceleration_vector

def apply_collisions(molecules):
        # Bind the molecules to the bounding box
    for i in range(len(molecules["points"])):
        if molecules["points"][i][0] < 0:
            molecules["points"][i][0] = 0
        if molecules["points"][i][0] > 10:
            molecules["points"][i][0] = 10
        if molecules["points"][i][1] < 0:
            molecules["points"][i][1] = 0
        if molecules["points"][i][1] > 10:
            molecules["points"][i][1] = 10
        if molecules["points"][i][2] < 0:
            molecules["points"][i][2] = 0
        if molecules["points"][i][2] > 10:
            molecules["points"][i][2] = 10