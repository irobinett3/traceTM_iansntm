import csv
from collections import deque

# Function to read Turing machine description from a CSV file
def read_tm_csv(file_name):
    machine_description = {}
    transitions = []

    # Read the CSV file
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Reading the header lines to get machine parameters
        machine_description["name"] = next(reader)[0]  # Machine name

        # Reading the states from the CSV
        machine_description["states"] = []
        state_row = next(reader)
        for item in state_row:
            if item.strip() != '':
                machine_description["states"].append(item.strip()) 
        
        # Reading the input alphabet
        machine_description["input_alphabet"] = []
        input_row = next(reader)
        for item in input_row:
            if item.strip() != '':
                machine_description["input_alphabet"].append(item.strip()) 
        
        # Reading the tape alphabet
        machine_description["tape_alphabet"] = []
        tape_row = next(reader)
        for item in tape_row:
            if item.strip() != '':
                machine_description["tape_alphabet"].append(item.strip()) 

        # Reading start, accept, and reject states
        machine_description["start_state"] = next(reader)[0]  # Start state
        machine_description["accept_state"] = next(reader)[0]  # Accept state
        machine_description["reject_state"] = next(reader)[0]  # Reject state
        
        # Reading the transitions from the CSV
        for row in reader:
            if row:  # Make sure the row is not empty
                transitions.append({
                    "current_state": row[0],
                    "read_char": row[1],
                    "next_state": row[2],
                    "write_char": row[3],
                    "move_direction": row[4]
                })
    
    # Return the parsed machine description and transitions
    return machine_description, transitions


# Function to trace the behavior of a Non-deterministic Turing Machine (NTM)
def trace_ntm(machine_description, transitions, input_string, max_depth=100):
    tape = list(input_string) + ['_'] if not input_string.endswith('_') else list(input_string)
    head_position = 0  # Assuming the tape head starts at the middle (adjust as needed)
    initial_state = machine_description["start_state"]
    num_transitions = 0

    # Initialize the configuration queue with the starting state and tape
    configurations = deque([([tape[:], initial_state, head_position])])
    tree_of_configurations = []
    visited = set()

    for depth in range(max_depth):
        current_depth_configurations = []  # List of configurations at the current depth
        num_configurations_at_current_depth = len(configurations)

        # Process all configurations at the current depth
        for _ in range(num_configurations_at_current_depth):
            current_tape, current_state, current_head = configurations.popleft()

            # Extend the tape if the head goes out of bounds
            if current_head >= len(current_tape):
                current_tape.append('_')  # Extend to the right

            left_string = "".join(current_tape[:current_head])  # Left part of the tape
            right_string = "".join(current_tape[current_head:])  # Right part of the tape
            right_string = right_string.rstrip('_')  # Remove trailing blanks

            # Store the configuration at the current depth
            current_depth_configurations.append([left_string, current_state, right_string])

            # Check if this configuration has been visited already to avoid infinite loops
            config_tuple = tuple(current_tape), current_state, current_head
            if config_tuple in visited:
                continue
            visited.add(config_tuple)

            # Check if we reached an accept or reject state
            if current_state == machine_description["accept_state"]:
                tree_of_configurations.append(current_depth_configurations)
                return tree_of_configurations, True, num_transitions  # Accept state reached, return the tree
            elif current_state == machine_description["reject_state"]:
                continue  # Reject state reached, don't explore further from here
        
            if current_head < 0 or current_head >= len(current_tape):
                current_depth_configurations.append([left_string, machine_description["reject_state"], right_string])
                continue  # Skip out-of-bounds configurations

            # Add the current configuration to the tree

            # Get the symbol under the tape head
            current_symbol = current_tape[current_head]

            # Find all possible transitions from the current state and tape symbol
            possible_transitions = get_possible_transitions(transitions, current_state, current_symbol)
            if len(possible_transitions) == 0:
                possible_transitions = [(machine_description["reject_state"], current_symbol, 'S')]
            num_transitions += len(possible_transitions)

            # Generate new configurations based on the transitions
            for next_state, write_char, move_direction in possible_transitions:
                new_tape = current_tape[:]
                new_tape[current_head] = write_char  # Write the new character to the tape
                
                # Calculate the new head position
                if move_direction == 'L':
                    new_head = current_head - 1
                elif move_direction == 'R':
                    new_head = current_head + 1
                else:
                    new_head = current_head  # Stay in place
                
                # Add the new configuration to the queue
                configurations.append((new_tape, next_state, new_head))

        # Add configurations at this depth level to the tree
        if current_depth_configurations:
            tree_of_configurations.append(current_depth_configurations)

        # Stop if there are no configurations left to process
        if not configurations:
            break

    return tree_of_configurations, False, num_transitions


# Function to get possible transitions from the machine's transition table
def get_possible_transitions(transitions, state, char):
    """
    Returns all possible transitions for the given state and character from the machine description.
    
    Parameters:
    - transitions: the NTM's transitions.
    - state: Current state of the machine.
    - char: The character under the tape head.
    
    Returns:
    - A list of tuples (next_state, write_char, move_direction).
    """
    possible_transitions = []
    for transition in transitions:
        if transition["current_state"] == state and transition["read_char"] == char:
            possible_transitions.append((transition["next_state"], transition["write_char"], transition["move_direction"]))

    return possible_transitions



def main():
    # Input string for the Turing machine
    input_string = "abcaabas"
    input_file = 'csv_tests/abc_star.csv'
    
    # Open the output.txt file for writing
    with open('output.txt', 'w') as f:
        # Read the machine description and transitions from the CSV
        machine_description, transitions = read_tm_csv(input_file)

        # Trace the machine behavior on the input string
        tree, accepted, num_transitions = trace_ntm(machine_description, transitions, input_string)

        # Write the machine details to the output file
        f.write(f"Input String: {input_string}\n")
        f.write(f"Machine Name: {machine_description['name']}\n")
        f.write(f"Machine States: {machine_description['states']}\n")
        f.write(f"Input Alphabet: {machine_description['input_alphabet']}\n")
        f.write(f"Tape Alphabet: {machine_description['tape_alphabet']}\n")
        f.write(f"Start State: {machine_description['start_state']}\n")
        f.write(f"Accept State: {machine_description['accept_state']}\n")
        f.write(f"Reject State: {machine_description['reject_state']}\n")

        # Write the configuration tree at each depth
        for depth, configurations in enumerate(tree):
            f.write(f"Depth {depth}: {configurations}\n")

        # Write whether the string was accepted or not
        if accepted:
            f.write(f'String accepted at depth: {depth}\n')
        else:
            f.write(f'String was not accepted, proceeded to depth: {depth}\n')

        # Write the number of transitions taken during the execution
        f.write(f'Number of transitions taken: {num_transitions}\n')


if __name__ == "__main__":
    main()