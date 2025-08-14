# Importing modules
import pandas as pd
import os, sys
import re
import shutil
import time
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import scipy.sparse as sp
import glob
import torch
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import argparse
from distutils.util import strtobool


# ----------------------------------------------------------------------------------------------------------------
# Parsing arguments

def parse_args():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--modelParams-file", default = './Intel/modelParams_Intel.config')
    parser.add_argument("--power-data-csv", default = '../aminhaji/MLCAD_MLPACT/power_data.csv')
    parser.add_argument("--train-dir", default = './grid100_outputs/train')
    parser.add_argument("--test-dir", default = './grid100_outputs/test/')
    parser.add_argument("--visualize", type = lambda x: bool(strtobool(x)), default = False)
    parser.add_argument("--n-components-features", type = int, default = 100)
    parser.add_argument("--n-components-targets", type = int, default = 100)
    
    args = parser.parse_args()
    user_args = vars(args)
    
    return user_args

# ----------------------------------------------------------------------------------------------------------------
# Extracts parameter values from modelParams config file

def extract_value(path, key, var_name = None):
    
    # Scan "path" for a line that matches the "key" and return the value
    
    pattern = re.compile(rf'^\s*{re.escape(key)}\s*=\s*([0-9]*\.?[0-9]+)')
    with open(path, 'r') as file:
        for line in file:
            match = pattern.match(line)
            if match:
                value = float(match.group(1))
           #    print(f"{var_name} = {value}")   #prints value of value - optional, mostly used for testing function code
                return value

# extracting values:
    # num_sim_steps = 
    # int(extract_value(args.modelParams_file, 'total_simulation_time') / extract_value(args.modelParams_file, 'step_size'))

# ----------------------------------------------------------------------------------------------------------------
# Parsing power data from .cif files (input to PACT) - for training

def input_pact_parse(args, input_file):
    
    grid_height = int(extract_value(args['modelParams_file'], 'rows'))
    grid_width = int(extract_value(args['modelParams_file'], 'cols'))
    layers = int(extract_value(args['modelParams_file'], 'layer'))
    
    with open(input_file, 'r') as file:
        content = file.readlines()

    pattern = r'I_(\d+)_(\d+)_(\d+)\s+GND\s+\w+\s+PWL\((.*?)\)'

    # Dict to store data: {time_step: {(layer,row,col):value}}
    parsed_values = {}

    # Collect all time steps found in the file
    all_time_steps = set()

    for line in content:
        match = re.search(pattern, line)
        if match:
            layer, row, column = int(match.group(1)), int(match.group(2)), int(match.group(3))
            pwl_values = match.group(4).split()
            
            for i in range(0, len(pwl_values), 2):
                time_step = float(pwl_values[i].rstrip('s'))
                value = float(pwl_values[i+1].rstrip('A'))
                
                all_time_steps.add(time_step)
                if time_step not in parsed_values:
                    parsed_values[time_step] = {}
                parsed_values[time_step][(layer, row, column)] = value

    # Sort time steps
    sorted_time_steps = sorted(all_time_steps)

    # Generate grid keys only once
    grid_keys = [(layer, row, column)
                 for layer in range(layers)
                 for row in range(grid_height)
                 for column in range(grid_width)]

    # Prepare final structured array
    power_data_array = []

    for time_step in sorted_time_steps:
        timestep_values = parsed_values.get(time_step, {})
        # Fill missing grid entries with 0
        grid_values = [timestep_values.get(key, 0.0) for key in grid_keys]
        power_data_array.append(grid_values)

    df = pd.DataFrame(power_data_array, index=sorted_time_steps)
    df.to_csv(args['power_data_csv'], index_label='time_step')

    return df

# ----------------------------------------------------------------------------------------------------------------
# Parse temperature data from CSV files (for training)

def parse_temperature(args, file):
    df = pd.read_csv(file)
    grid_height = int(extract_value(args['modelParams_file'], 'rows'))
    grid_width = int(extract_value(args['modelParams_file'], 'cols'))
    temperature_values = df.iloc[:, 1:10001].values  # only first layer (100x100 grid = 10,000 columns)
    temperature_series_first_layer = temperature_values.reshape((-1, grid_height, grid_width))
    return temperature_series_first_layer

# ----------------------------------------------------------------------------------------------------------------
# loading the training data - This section of the code focuses on loading multiple power and temperature sequences from a specified directory, converting them into PyTorch tensors, and ensuring they have a consistent number of timesteps.

def load_train_data(args):

    # Directory containing .cir files
    cir_directory = args['train_dir']
    grid_height = int(extract_value(args['modelParams_file'], 'rows'))
    grid_width = int(extract_value(args['modelParams_file'], 'cols'))
    # List to store power tensors
    power_tensors = []
    temp_tensors = []
    count = 0
    num_sim_steps = 285*2
    # Iterate over all .cir files in the directory
    for filename in os.listdir(cir_directory):
        if filename.endswith('.cir'):
            file_path = os.path.join(cir_directory, filename)
            print('\n',file_path)
            df = input_pact_parse(args, file_path)
            power_data = df.values  # shape: (num_timesteps, num_power_nodes)
            num_timesteps = power_data.shape[0]
            power_tensor = torch.tensor(power_data, dtype=torch.float32)
            power_tensor = power_tensor.view(num_timesteps, grid_height, grid_width)
            if power_tensor.shape[0] < num_sim_steps:    # makes sure all power tensors conform to num_sim_steps
                last_power = power_tensor[-1:].clone()  # shape [1, 100, 100]
                extra_steps = num_sim_steps - power_tensor.shape[0]
                extended_power = torch.cat([power_tensor, last_power.repeat(extra_steps, 1, 1)], dim=0)
            else:
                extended_power = power_tensor
            power_tensors.append(extended_power)
            file_path_new = os.path.join(file_path + '.csv')    # loading temperature datas
            print('\n',file_path_new)
            df_temp = parse_temperature(args, file_path_new)
            temp_tensor = torch.tensor(df_temp, dtype=torch.float32)
            temp_tensors.append(temp_tensor)
            count += 1
        if count == 10:    #change count to however many .cir/.csv pairs there are in the training folder
            break

    if power_tensors:
        print(power_tensors[0].shape)
        print(temp_tensors[0].shape)
    else:
        print("No .cir files found in the directory.")
    
    return power_tensors, temp_tensors

# ----------------------------------------------------------------------------------------------------------------
# Training model

def train_model(args, power_tensors, temp_tensors):
    
    # -------------------------------
    # Assume you have already loaded your data:
    # power_tensors: list of torch tensors with shape (num_transitions, H, W)
    # temp_tensors:  list of torch tensors with shape (num_transitions+1, H, W)
    #
    # For example:
    #   - H, W = 128, 128
    #   - num_transitions = 284 (so each power tensor is (284, 128, 128)
    #     and each temp tensor is (285, 128, 128))
    # -------------------------------
    num_transitions = 569  # number of transitions per sample
    H, W = int(extract_value(args['modelParams_file'], 'rows')), int(extract_value(args['modelParams_file'], 'cols'))   # grid dimensions

    # -------------------------------
    # Prepare training data: X_train are features formed by concatenating power at t+1 and temp at t;
    # y_train are targets, i.e. temperature at t+1.
    # -------------------------------
    start_time = time.time()
    X_train = []
    y_train = []
    count = 0
    for sample_idx in range(len(power_tensors)):
        power_seq = power_tensors[sample_idx]
        temp_seq  = temp_tensors[sample_idx]

        for t in range(num_transitions):
            # Flatten the (H,W) maps to vectors
            power_np = power_seq[t+1].clone().detach().cpu().numpy().flatten()
            temp_np  = temp_seq[t].clone().detach().cpu().numpy().flatten()
            feature  = np.concatenate((power_np, temp_np))

            target = temp_seq[t+1].clone().detach().cpu().numpy().flatten()

            X_train.append(feature)
            y_train.append(target)
        count += 1
        if count == 15:
            break

    X_train = np.array(X_train)  # shape: (num_samples, 2*H*W)
    y_train = np.array(y_train)  # shape: (num_samples, H*W)

    # -------------------------------
    # Standardize the data
    # -------------------------------
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()

    X_train_scaled = scaler_X.fit_transform(X_train)
    y_train_scaled = scaler_y.fit_transform(y_train)

    # -------------------------------
    # Apply PCA using scikit-learn
    # -------------------------------
    # Choose number of components (you may adjust these)
    n_components_features = args['n_components_features']
    n_components_targets  = args['n_components_targets']
    
    pca_features = PCA(n_components = n_components_features)
    X_train_reduced = pca_features.fit_transform(X_train_scaled)

    pca_targets = PCA(n_components = n_components_targets)
    y_train_reduced = pca_targets.fit_transform(y_train_scaled)

    # -------------------------------
    # Train the Linear Regression model in the reduced space using PyTorch
    # -------------------------------
    # Convert the PCA-reduced data to torch tensors.
    X_train_reduced_torch = torch.from_numpy(X_train_reduced).float()
    y_train_reduced_torch = torch.from_numpy(y_train_reduced).float()

    # Add an intercept (bias) term by concatenating a column of ones.
    N = X_train_reduced_torch.shape[0]
    ones = torch.ones((N, 1))
    X_design = torch.cat([X_train_reduced_torch, ones], dim=1)  # shape: (N, n_components_features + 1)

    # Compute regression weights in closed form using the pseudoinverse:
    # beta = (X_design^T X_design)^(-1) X_design^T y_train_reduced
    beta = torch.pinverse(X_design) @ y_train_reduced_torch  # shape: (n_components_features+1, n_components_targets)
    end_time = time.time()
    # Evaluate training performance in the reduced space
    predictions_reduced = X_design @ beta  # shape: (N, n_components_targets)
    mse_reduced = torch.mean((y_train_reduced_torch - predictions_reduced) ** 2).item()
    print("Training MSE in PCA target space:", mse_reduced)
    print("Training Time in Seconds:", end_time - start_time)
    # Optionally, convert predictions back to the original (scaled) target space and compute MSE.
    # We use scikit-learn’s inverse_transform methods.
    predictions_reduced_np = predictions_reduced.clone().detach().cpu().numpy()
    predictions_scaled = pca_targets.inverse_transform(predictions_reduced_np)
    mse_original = mean_squared_error(y_train_scaled, predictions_scaled)
    print("Training MSE in original target space (scaled):", mse_original)

    return scaler_X, pca_features, beta, pca_targets, scaler_y

# ----------------------------------------------------------------------------------------------------------------
# Training continued

# -------------------------------
# Define a function to predict the next temperature map
# -------------------------------
def predict_next_temp(args, power_map, current_temp, scaler_X, pca_features, beta, pca_targets, scaler_y):
    
    H, W = int(extract_value(args['modelParams_file'], 'rows')), int(extract_value(args['modelParams_file'], 'cols'))   # grid dimensions

    """
    Predict the next temperature map given a power map and the current temperature map.
    
    Parameters:
        power_map: torch tensor of shape (H, W) representing power at time t+1.
        current_temp: torch tensor of shape (H, W) representing temperature at time t.
    
    Returns:
        Predicted temperature map as a numpy array of shape (H, W) for time t+1.
    """
    
    # Convert input maps to numpy arrays and flatten
    power_np = power_map.clone().detach().cpu().numpy().flatten()

    # Handles if current_temp is a NumPy array or a PyTorch tensor
    if isinstance(current_temp, torch.Tensor):
        # If it's a PyTorch tensor, convert it to NumPy
        temp_np = current_temp.detach().cpu().numpy().flatten()
    elif isinstance(current_temp, np.ndarray):
        # If it's already a NumPy array, just flatten it
        temp_np = current_temp.flatten()
    else:
        # Handle unexpected types (optional, but good for robustness)
        raise TypeError(f"current_temp has unexpected type: {type(current_temp)}")   
        
    feature = np.concatenate((power_np, temp_np)).reshape(1, -1)
    
    # Standardize the feature using the previously fitted scaler
    feature_scaled = scaler_X.transform(feature)
    
    # Project the scaled feature using the PCA for features
    feature_reduced = pca_features.transform(feature_scaled)  # shape: (1, n_components_features)
    
    # Append bias term for the intercept
    feature_design = np.concatenate([feature_reduced, np.ones((1, 1))], axis=1)
    
    # Convert to torch tensor and predict in the reduced target space
    feature_design_torch = torch.from_numpy(feature_design).float()
    pred_reduced_torch = feature_design_torch @ beta  # shape: (1, n_components_targets)
    
    # Convert the prediction to numpy and invert the PCA transformation on the target
    pred_reduced = pred_reduced_torch.clone().detach().cpu().numpy()
    pred_scaled = pca_targets.inverse_transform(pred_reduced)
    
    # Inverse the scaling to obtain the final prediction
    pred_original = scaler_y.inverse_transform(pred_scaled)
    
    return pred_original.reshape(H, W)

# ----------------------------------------------------------------------------------------------------------------
# making prediction + visualization


def predict_temp_on_one_file(args, file_name, scaler_X, pca_features, beta, pca_targets, scaler_y):

    df = input_pact_parse(args, args['test_dir'] + file_name)
    power_data = df.values  # shape: (num_timesteps, num_power_nodes)
    num_timesteps_power = power_data.shape[0]
    print(num_timesteps_power)
    print(power_data.shape)

    # Define grid dimensions (should match training dimensions)
    grid_height, grid_width = int(extract_value(args['modelParams_file'], 'rows')), int(extract_value(args['modelParams_file'], 'cols'))

    # Reshape the power data to (num_timesteps, grid_height, grid_width)
    power_array = power_data.reshape(num_timesteps_power, grid_height, grid_width)

    # Define the number of simulation steps (num_sim_steps) for your rollout
    num_sim_steps = 285*2  # example; adjust as needed

    # Extend the power sequence if needed so it has num_sim_steps timesteps
    if power_array.shape[0] < num_sim_steps:
        last_power = power_array[-1:].copy()  # shape: (1, grid_height, grid_width)
        extra_steps = num_sim_steps - power_array.shape[0]
        extended_power = np.concatenate([power_array, np.repeat(last_power, extra_steps, axis = 0)], axis = 0)
    else:
        extended_power = power_array
    extended_power = torch.tensor(extended_power, dtype = torch.float32)
    # power_tensors.append(extended_power)
    test_power_seq = extended_power  # shape: (T, grid_height, grid_width)
    num_timesteps_power = test_power_seq.shape[0]

    assert num_timesteps_power == num_sim_steps
    print(test_power_seq.shape)
          
      
    # --- Rollout Prediction ---
    # Initialize the predicted sequence with the first temperature state.
    start_rollout = time.time()
    predicted_seq = []

    initial_temp = torch.full((grid_height, grid_width), 318.15, dtype = torch.float32) # setting initial temperture to be room temp
    curr_temp = initial_temp

    for t in range(min(test_power_seq.shape[0], num_sim_steps) - 1):
        curr_power = test_power_seq[t+1]

        # Ensure curr_temp is a PyTorch tensor before passing to predict_next_temp
        # If curr_temp is already a numpy array from a previous prediction, convert it back to tensor.

        if isinstance(curr_power, np.ndarray):
            power_tensor = torch.tensor(curr_power, dtype = torch.float32)
        else:
            power_tensor = curr_power.clone().detach().to(torch.float32)    

        if isinstance(curr_temp, np.ndarray):
            temp_tensor = torch.tensor(curr_temp, dtype = torch.float32)
        else: # It's already a torch tensor (like initial_uniform_temp)
            temp_tensor = curr_temp.clone().detach().to(torch.float32)

        next_temp = predict_next_temp(args, power_tensor, temp_tensor, scaler_X, pca_features, beta, pca_targets, scaler_y)
        predicted_seq.append(next_temp)
        curr_temp = next_temp

    end_rollout = time.time()

    print("Total rollout inference time: {:.6f} seconds".format(end_rollout - start_rollout))


    # Convert the list of predictions into an array with shape (T, grid_height, grid_width)
    predicted_seq = np.stack(predicted_seq)        
    
    return predicted_seq

# ----------------------------------------------------------------------------------------------------------------
# iterating prediction over all test files and saving temp predictions

def predict_temp_for_all_files(args, scaler_X, pca_features, beta, pca_targets, scaler_y):
    
    # List all files in the specified directory, using glob.glob to do a filesystem search
    all_test_files = glob.glob(os.path.join(args['test_dir'], '*.cir'))

    for test_file in all_test_files:
        test_file_name = os.path.basename(test_file)
        print(test_file_name)
        predicted_temp = predict_temp_on_one_file(args, test_file_name, scaler_X, pca_features, beta, pca_targets, scaler_y)

        
        if args['visualize']:
            # --- Visualization ---
            # Plot a few selected timesteps to compare predictions with ground truth
            time_steps_to_plot = [1, 2, 30, 400]
            plt.figure(figsize=(12, 8))

            for i, t in enumerate(time_steps_to_plot):
                plt.subplot(2, len(time_steps_to_plot), i+1)
                plt.title(f"Predicted t = {t}")
                plt.imshow(predicted_temp[t], cmap="hot")
                plt.colorbar()
                # Saving image to a folder with the same name as the test file
                save_dir = args['test_dir'] + 'MLCAD_predicted_results/' + test_file_name
                os.makedirs(save_dir, exist_ok = True)
                saved_image_path = os.path.join(save_dir, f"{t}.png")
                plt.savefig(saved_image_path)

            plt.tight_layout()
            plt.show()

            
        else:
            # Saving predicted temperature into a .csv file
            T, X, Y =  predicted_temp.shape[0], predicted_temp.shape[1], predicted_temp.shape[2]
            flat = predicted_temp.reshape(T, X * Y)

            csv_dir = glob.glob(os.path.join(args['train_dir'], "*.csv"))
            model_csv_path = csv_dir[0]
            model_csv_header = pd.read_csv(model_csv_path, nrows = 0)
            time_col = pd.read_csv(model_csv_path, usecols = ["TIME"])["TIME"]
            df = pd.DataFrame(flat, columns = model_csv_header.columns[1 : X * Y + 1])
            df.insert(0, "TIME", time_col)

            df.to_csv(args['test_dir'] + 'MLCAD_predicted_results/' + test_file_name + "_result.csv", index = False)   

# ----------------------------------------------------------------------------------------------------------------
# MAIN function

def main():
    args = parse_args()
    
    power_tensors, temp_tensors = load_train_data(args)
    scaler_X, pca_features, beta, pca_targets, scaler_y = train_model(args, power_tensors, temp_tensors)
    predict_temp_for_all_files(args, scaler_X, pca_features, beta, pca_targets, scaler_y)    

    
if __name__ == "__main__":
    main()    
    