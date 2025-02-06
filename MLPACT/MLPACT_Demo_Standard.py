"""
MLPACT-Standard

This script runs a PACT simulation and then uses an online-trained linear regression
model to predict temperature from power input data. The simulation runs in 3D mode and
the model is updated continuously until convergence.
"""

# Import necessary libraries
import os
import time
import glob
import re
import shutil
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import argparse

# Global configuration defaults
DEFAULT_MATRIX_SHAPE = (128, 128)
TOTAL_SAMPLES = 150            # Total number of iterations to process
ACCURACY_THRESHOLD = 0.05      # A prediction is considered accurate if error is below this threshold

# Global variables for ML training state
accurate_predictions = 0
X_train = []
y_train = []
max_errors = []
mse_list = []
mae_list = []

# Initialize the linear regression model
model = LinearRegression()


def read_format_input(file_path, n_rows, n_cols):
    """
    Read the CSV file and extract columns of the form V(NODE0_row_col).
    """
    print(f"Reading CSV file: {file_path} with dimensions ({n_rows}, {n_cols})")
    columns = [f'V(NODE0_{row}_{col})' for row in range(n_rows) for col in range(n_cols)]
    df = pd.read_csv(file_path, usecols=columns)
    return df

def read_format_input_3D(layers, file_path, n_rows, n_cols):
    """
    Read the CSV file for each layer in 3D mode and concatenate the flattened vectors.
    
    Args:
        layers (list): List of layer indices to process.
        file_path (str): Path to the CSV file.
        n_rows (int): Number of rows in the grid.
        n_cols (int): Number of columns in the grid.
        
    Returns:
        pd.Series: A concatenated vector of values from all layers.
    """
    df_list = []
    for layer in layers:
        # Generate column names for the specific layer
        columns = [f'V(NODE{layer}_{row}_{col})' for row in range(n_rows) for col in range(n_cols)]
        # Read the specified columns from the file
        df_layer = pd.read_csv(file_path, usecols=columns)
        # Flatten the dataframe into a vector
        df_list.append(df_layer.values.flatten())
    # Concatenate all layers' vectors
    concatenated_vector = pd.concat([pd.Series(vector) for vector in df_list], axis=0)
    return concatenated_vector


def online_train_and_predict(pact_output, pact_input, accuracy_threshold=ACCURACY_THRESHOLD):
    """
    Incrementally train the model and predict the output.
    
    Args:
        pact_output (np.array): The true output vector from PACT.
        pact_input (np.array): The input vector used for prediction.
        accuracy_threshold (float): The threshold for considering a prediction accurate.
        
    Returns:
        tuple: (prediction, convergence flag, normalized error)
    """
    global accurate_predictions, X_train, y_train, max_errors, mse_list, mae_list, model

    # Add new data to the training set
    X_train.append(pact_input)
    y_train.append(pact_output)

    # Convert lists to numpy arrays for training
    X_train_np = np.array(X_train)
    y_train_np = np.array(y_train)
    
    # Train the model incrementally until a few accurate predictions are reached
    if accurate_predictions < 2:
        print("Training model...")
        model.fit(X_train_np, y_train_np)

    # Predict the next output based on the last input
    prediction = model.predict([pact_input])[0]

    # print('Input:', pact_input)
    # print('Prediction:', prediction)
    # print('True Value:', pact_output)
    # Calculate prediction error
    error = np.abs(prediction - pact_output)
    max_error = np.max(error)
    max_errors.append(max_error)
    mse = np.mean((prediction - pact_output) ** 2)
    mae = np.mean(error)
    mse_list.append(mse)
    mae_list.append(mae)

    print('Error is:', mae)
    print('Max Error is:', max_error)

    # Update convergence counter based on the error threshold
    if np.all(error <= accuracy_threshold):
        accurate_predictions += 1
        flag = True
    else:
        accurate_predictions -= 1
        flag = False

    normalized_error = np.sum(error) / (DEFAULT_MATRIX_SHAPE[0] * DEFAULT_MATRIX_SHAPE[1])
    
    # Convergence is declared after 3 consecutive accurate predictions
    if accurate_predictions >= 3:
        return prediction, True, normalized_error
    else:
        return prediction, False, normalized_error

def input_pact_parse(input_file, matrix_shape=DEFAULT_MATRIX_SHAPE):
    """
    Parse the PACT input file.
    Expects lines formatted like:
      I_layer_row_column GND <something> <value>A
    Missing entries are filled with 0.
    """
    with open(input_file, 'r') as file:
        content = file.readlines()

    pattern = r'I_(\d+)_(\d+)_(\d+)\s+GND\s+\w+\s+([+-]?\d*\.?\d+[eE]?[+-]?\d*)A'
    parsed_values = {}
    for line in content:
        match = re.search(pattern, line)
        if match:
            layer = int(match.group(1))
            row = int(match.group(2))
            col = int(match.group(3))
            value = float(match.group(4))
            parsed_values[(layer, row, col)] = value

    rows, cols = matrix_shape
    all_entries = {(0, row, col) for row in range(rows) for col in range(cols)}
    missing_entries = all_entries - set(parsed_values.keys())
    for entry in missing_entries:
        parsed_values[entry] = 0.0

    sorted_values = [parsed_values[(0, row, col)] for row in range(rows) for col in range(cols)]
    return sorted_values


def input_pact_parse_3D(input_file, matrix_shape=DEFAULT_MATRIX_SHAPE):
    """
    Parse the PACT simulation output file in 3D mode.
    Expected format for each line:
      I_layer_row_column GND <something> <value>A
    
    Args:
        input_file (str): Path to the PACT output file.
        matrix_shape (tuple): Shape of the 2D grid.
        
    Returns:
        tuple: (concatenated_values, active_layers)
    """
    with open(input_file, 'r') as file:
        content = file.readlines()

    pattern = r'I_(\d+)_(\d+)_(\d+)\s+GND\s+\w+\s+([+-]?\d*\.?\d+[eE]?[+-]?\d*)A'
    parsed_values = {}
    active_layers = []

    rows, cols = matrix_shape
    # Extract values for each layer
    for line in content:
        match = re.search(pattern, line)
        if match:
            layer, row, col, value = int(match.group(1)), int(match.group(2)), int(match.group(3)), float(match.group(4))
            if layer not in parsed_values:
                parsed_values[layer] = {}
                active_layers.append(layer)
            parsed_values[layer][(row, col)] = value

    concatenated_values = []
    # Process each layer's data
    for layer in sorted(parsed_values.keys()):
        # Generate the complete set of grid entries (rowsxcols)
        all_entries = {(row, col) for row in range(rows) for col in range(cols)}
        missing_entries = all_entries - parsed_values[layer].keys()
        for entry in missing_entries:
            parsed_values[layer][entry] = 0.0  # Fill missing entries with 0
        sorted_values = [parsed_values[layer][(row, col)] for row in range(rows) for col in range(cols)]
        concatenated_values.extend(sorted_values)
    
    return concatenated_values, active_layers

def run_simulation(ptraces_directory, ml_dataset_directory, max_iterations=TOTAL_SAMPLES, mode='2D'):
    global accurate_predictions, X_train, y_train, max_errors, mse_list, mae_list, model
    counter = 0
    total_pact_simulation_time = 0
    total_ml_simulation_time = 0  # This is the correctly initialized variable
    total_error = 0

    # Change to ML dataset directory
    original_dir = os.getcwd()
    os.chdir(ml_dataset_directory)
    if mode == '3D':
        for folder_name in os.listdir(ptraces_directory):
            folder_path = os.path.join(ptraces_directory, folder_name)
            if os.path.isdir(folder_path):
                for file_name in os.listdir(folder_path):
                    if file_name.startswith('scaled_') and file_name.endswith('.csv'):
                        src_file_path = os.path.join(folder_path, file_name)
                        dst_file_path = os.path.join('tier0_ptrace_2lay.csv')
                        shutil.copy(src_file_path, dst_file_path)

                        ptrace = pd.read_csv(dst_file_path)
                        ptrace = pd.concat(
                            [ptrace['UnitName'], (ptrace.drop(columns=['UnitName']).mean(axis=1))],
                            axis=1,
                            keys=['UnitName', 0]
                        )
                        ptrace = ptrace.T
                        ptrace.columns = ptrace.iloc[0]
                        ptrace = ptrace[1:]

                        start_time = time.time()
                        os.system("module load python3/3.6.5 gcc/5.5.0 fftw/3.3.8 netcdf/4.6.1 "
                                  "blis/0.6.0 openmpi/3.1.4 xyce/6.12 && "
                                  "python ../PACT/src/PACT.py M3D_lcf_2.csv Intel.config modelParams_Intel_2lay.config "
                                  "--gridSteadyFile M3D_new.grid.steady > /dev/null 2>&1"
                                  )
                        end_time = time.time()
                        pact_time = end_time - start_time
                        print(f"PACT simulation execution time: {pact_time:.2f} seconds")
                        total_pact_simulation_time += pact_time

                        power_matrix, layers = input_pact_parse_3D('M3D_new.cir')
                        temp_node = read_format_input_3D(layers, 'M3D_new.cir.csv', DEFAULT_MATRIX_SHAPE[0], DEFAULT_MATRIX_SHAPE[1])
                        vector_output = temp_node.values.flatten()

                        start_time = time.time()
                        pred_temp, flag, error = online_train_and_predict(vector_output, power_matrix)
                        total_error += error 
                        end_time = time.time()
                        # Use the correctly named variable here
                        total_ml_simulation_time += (end_time - start_time)
                        print(f"Execution time for ML: {end_time - start_time:.2f} seconds")
                        counter += 1
                    if counter == max_iterations:
                        break
    elif mode == '2D':
        for folder_name in os.listdir(ptraces_directory):
            folder_path = os.path.join(ptraces_directory, folder_name)
            if os.path.isdir(folder_path):
                for file_name in os.listdir(folder_path):
                    if file_name.startswith('scaled_') and file_name.endswith('.csv'):
                        src_file_path = os.path.join(folder_path, file_name)
                        dst_file_path = os.path.join('tier0_ptrace_gen.csv')
                        shutil.copy(src_file_path, dst_file_path)
                        
                        ptrace = pd.read_csv(dst_file_path)
                        ptrace = pd.concat(
                            [ptrace['UnitName'], (ptrace.drop(columns=['UnitName']).mean(axis=1))],
                            axis=1,
                            keys=['UnitName', 0]
                        )
                        ptrace = ptrace.T
                        ptrace.columns = ptrace.iloc[0]
                        ptrace = ptrace[1:]

                        start_time = time.time()
                        os.system(
                            "module load python3/3.6.5 gcc/5.5.0 fftw/3.3.8 netcdf/4.6.1 "
                            "blis/0.6.0 openmpi/3.1.4 xyce/6.12 && "
                            "python ../PACT/src/PACT.py Intel_lcf.csv Intel.config modelParams_Intel.config "
                            "--gridSteadyFile example.grid.steady > /dev/null 2>&1"
                        )
                        end_time = time.time()
                        pact_time = end_time - start_time
                        print(f"PACT simulation execution time: {pact_time:.2f} seconds")
                        total_pact_simulation_time += pact_time

                        power_matrix = input_pact_parse('example.cir')
                        print(len(power_matrix))
                        temp_node = read_format_input('example.cir.csv', DEFAULT_MATRIX_SHAPE[0], DEFAULT_MATRIX_SHAPE[1])
                        vector_output = temp_node.values.flatten()

                        start_time = time.time()
                        pred_temp, flag, error = online_train_and_predict(vector_output, power_matrix)
                        total_error += error 
                        end_time = time.time()
                        # Again, use the correctly named variable
                        total_ml_simulation_time += (end_time - start_time)
                        print(f"Execution time for ML: {end_time - start_time:.2f} seconds")
                        counter += 1
                    if counter == max_iterations:
                        break

    print("Total PACT simulation time:", total_pact_simulation_time)
    print("Total ML simulation time:", total_ml_simulation_time)

    os.chdir(original_dir)


def main():
    parser = argparse.ArgumentParser(description="MLPACT")
    parser.add_argument(
        "--ptraces_dir",
        type=str,
        default="different_ptraces",
        help="Directory containing ptrace folders",
    )
    parser.add_argument(
        "--ml_dataset_dir",
        type=str,
        default="ML_Dataset",
        help="Directory for ML dataset",
    )
    parser.add_argument(
        "--max_iterations",
        type=int,
        default=50,
        help="Maximum number of iterations to run the simulation",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="2D",
        help="Simulation mode: 3D or 2D",
    )
    args = parser.parse_args()

    run_simulation(args.ptraces_dir, args.ml_dataset_dir, args.max_iterations, args.mode)

if __name__ == "__main__":
    main()

