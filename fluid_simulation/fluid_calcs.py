import numpy as np

# Here each molecule is compared to every other molecule, which is not efficient, but easy to implement

# molecule = [position_vec3, velocity_vec3]
def step_fluid_sim(molecules):

    accelerations = np.zeros((len(molecules["points"]), 3))

    for i in range(len(molecules["points"])):
        acceleration_vector = get_molecule_acceleration(molecules["points"][i], molecules["points"])
        accelerations[i] = acceleration_vector
    print(accelerations[0])

    # Apply the accelerations to the molecules' velocities
    #molecules["velocities"] += accelerations
    print(molecules["velocities"][0])
    
    # Apply the velocities to the molecules' positions
    molecules["points"] += accelerations
    print(molecules["points"][0])

    return molecules

def get_molecule_acceleration(molecule_pos, molecules_pos):
    acceleration_vector = np.zeros(3)

    for temp_molecule_pos in molecules_pos:
        # Kinda stupid for two molecules to be in the same place, but it's possible and it won't handle it
        if(np.array_equal(temp_molecule_pos, molecule_pos)):
            continue
        # Get the vector between the main molecule and the temp molecule
        vector = molecule_pos - temp_molecule_pos

        # Get the distance between the two molecules
        distance = np.linalg.norm(vector)

        # Normalize the vector
        vector /= np.linalg.norm(vector)
        # Apply the force to the main molecule based on the distance
        acceleration_vector += vector / 100 # Displacement vector inversely exponential to distance
    
    return acceleration_vector