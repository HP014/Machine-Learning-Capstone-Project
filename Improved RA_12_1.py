import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, Matern
from sklearn.gaussian_process.kernels import WhiteKernel
from scipy.stats import norm
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# Import our visualization functions
from plotting_utils import (
    expected_improvement, plot_gp_1d, plot_acquisition_1d, plot_bo_iteration_1d,
    plot_2d_function, plot_2d_bo_state, plot_convergence,
    plot_parallel_coordinates, upper_confidence_bound
)

# Set random seed for reproducibility
np.random.seed(42)
plt.style.use('seaborn-v0_8-darkgrid')  

# Load the updated inputs and outputs for each function from the required week. Make sure to change path as required. 
func1_inputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_1\\updated_inputs.npy')
func1_outputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_1\\updated_outputs.npy')

func2_inputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_2\\updated_inputs.npy')
func2_outputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_2\\updated_outputs.npy')

func3_inputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_3\\updated_inputs.npy')
func3_outputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_3\\updated_outputs.npy')

func4_inputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_4\\updated_inputs.npy')
func4_outputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_4\\updated_outputs.npy')

func5_inputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_5\\updated_inputs.npy')
func5_outputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_5\\updated_outputs.npy')

func6_inputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_6\\updated_inputs.npy')
func6_outputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_6\\updated_outputs.npy')

func7_inputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_7\\updated_inputs.npy')
func7_outputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_7\\updated_outputs.npy')

func8_inputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_8\\updated_inputs.npy')
func8_outputs = np.load('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_8\\updated_outputs.npy')



# Check the shapes and basic info for all functions
functions = {
    'func1': (func1_inputs, func1_outputs),
    'func2': (func2_inputs, func2_outputs),
    'func3': (func3_inputs, func3_outputs),
    'func4': (func4_inputs, func4_outputs),
    'func5': (func5_inputs, func5_outputs),
    'func6': (func6_inputs, func6_outputs),
    'func7': (func7_inputs, func7_outputs),
    'func8': (func8_inputs, func8_outputs),
}

for name, (inputs, outputs) in functions.items():
    print(f"{name}: inputs {inputs.shape}, outputs {outputs.shape}")

def analyze_function(name, inputs, outputs):
    #Find the best point and basic statistics
    best_idx = np.argmax(outputs)
    best_output = outputs[best_idx]
    best_input = inputs[best_idx]
    
    print(f"\n{name}:")
    print(f"  - Dimensions: {inputs.shape[1]}D")
    print(f"  - Data points: {len(outputs)}")
    print(f"  - Output range: [{outputs.min():.4f}, {outputs.max():.4f}]")
    print(f"  - Best output: {best_output:.4f}")
    print(f"  - Best input: {best_input}")
    
    return best_idx, best_input, best_output

# Analyze all functions
best_points = {}
for name, (inputs, outputs) in functions.items():
    idx, inp, out = analyze_function(name, inputs, outputs)
    best_points[name] = {'idx': idx, 'input': inp, 'output': out}


#To store and append new data points. This will be useful for week 1 and beyond.
#Steps for each week to append new inputs and outputs and save in a new folder for that week.
"""
1. Store the new queries and outputs in the below dictionary for easy access.
2. Change the week number in the below input and output names i.e week2_queries and week2_outputs to the current week number.
3. Change the week number in the appending/verification code below to the current week number.
4. In the data folder, create a new folder for the current week (e.g. Week_2) and inside that create empty subfolders for each function (function_1, function_2, ..., function_8).
5. In the code for saving the file, make sure to update the path to the new week folder (e.g. Week_2)
6. Once the code is run, make sure the above code for loading the new data is updated for the new week so it is not loading the previous week.
7. Once done, make sure to comment out the code for appending new data and verifying it so that it does not run again in the future. This is important to avoid duplicating data points.
"""


# Storing week 4 queries and outputs
week4_queries = {
    'func1': np.array([0.367783, 0.632306]),
    'func2': np.array([0.610276, 0.186098]),
    'func3': np.array([0.463239, 0.001444, 0.554394]),
    'func4': np.array([0.384555, 0.428957, 0.409752, 0.392875]),
    'func5': np.array([0.361593, 0.858023, 0.999172, 0.995664]),
    'func6': np.array([0.416990, 0.438821, 0.441447, 0.595086, 0.064306]),
    'func7': np.array([0.027866, 0.096790, 0.333634, 0.282039, 0.480875, 0.753752]),
    'func8': np.array([0.169427, 0.439645, 0.075814, 0.083122, 0.700520, 0.187213, 0.050099, 0.875971])
}

week4_outputs = {
    'func1': 3.8174845321185087e-34,
    'func2': 0.1499370998278185,
    'func3': -0.09316800572796659,
    'func4': 0.36752865304022864,
    'func5': 2986.9379783299123,
    'func6': -0.4694076565389275,
    'func7': 1.641567368351063,
    'func8': 9.7378440611899
}

print("\n" + "="*60)
print("WEEK 4 QUERIES AND OUTPUTS")
print("="*60)

print("\nWeek 4 Queries:")
for key, value in week4_queries.items():
    print(f"  {key}: {value}")

print("\nWeek 4 Outputs:")
for key, value in week4_outputs.items():
    print(f"  {key}: {value}")


"""
# =============================================================================
# Appending New Data And Verifying
# =============================================================================

# =============================================================================
# FUNCTION 1: APPEND NEW DATA
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 1: APPENDING NEW DATA")
print("="*60)

# APPENDING NEW DATA
func1_inputs = np.vstack([func1_inputs, week4_queries['func1']])
func1_outputs = np.append(func1_outputs, week4_outputs['func1'])

# AFTER APPENDING
print(f"\nAFTER:")
print(f"  Inputs shape: {func1_inputs.shape}")  # Now (11, 2)
print(f"  Outputs shape: {func1_outputs.shape}")  # Now (11,)
print(f"  New input point: {func1_inputs[-1]}")
print(f"  New output: {func1_outputs[-1]}")
print(f"  Last 3 inputs:\n{func1_inputs[-3:]}")

# VERIFY
print(f"\nVERIFY:")
print(f"  Expected new input: {week4_queries['func1']}")
print(f"  Match? {np.array_equal(func1_inputs[-1], week4_queries['func1'])}")
print(f"  Expected new output: {week4_outputs['func1']}")
print(f"  Match? {func1_outputs[-1] == week4_outputs['func1']}")
print(f"  Total points: {len(func1_outputs)}")

# =============================================================================
# FUNCTION 2: APPEND NEW DATA
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 2: APPENDING NEW DATA")
print("="*60)
# APPEND
func2_inputs = np.vstack([func2_inputs, week4_queries['func2']])
func2_outputs = np.append(func2_outputs, week4_outputs['func2'])

# AFTER APPENDING
print(f"\nAFTER:")
print(f"  Inputs shape: {func2_inputs.shape}")  # Now (11, 2)
print(f"  Outputs shape: {func2_outputs.shape}")  # Now (11,)
print(f"  New input point: {func2_inputs[-1]}")
print(f"  New output: {func2_outputs[-1]}")
print(f"  Last 3 inputs:\n{func2_inputs[-3:]}")

# VERIFY
print(f"\nVERIFY:")
print(f"  Expected new input: {week4_queries['func2']}")
print(f"  Match? {np.array_equal(func2_inputs[-1], week4_queries['func2'])}")
print(f"  Expected new output: {week4_outputs['func2']}")
print(f"  Match? {func2_outputs[-1] == week4_outputs['func2']}")
print(f"  Total points: {len(func2_outputs)}")


# =============================================================================
# FUNCTION 3: APPEND NEW DATA
# =============================================================================
print("\n" + "="*60)
print("FUNCTION 3: APPENDING NEW DATA")
print("="*60)
# APPEND
func3_inputs = np.vstack([func3_inputs, week4_queries['func3']])
func3_outputs = np.append(func3_outputs, week4_outputs['func3'])

# AFTER APPENDING
print(f"\nAFTER:")
print(f"  Inputs shape: {func3_inputs.shape}")  # Now (16, 3)
print(f"  Outputs shape: {func3_outputs.shape}")  # Now (16,)
print(f"  New input point: {func3_inputs[-1]}")
print(f"  New output: {func3_outputs[-1]}")

# VERIFY
print(f"\nVERIFY:")
print(f"  Expected new input: {week4_queries['func3']}")
print(f"  Match? {np.array_equal(func3_inputs[-1], week4_queries['func3'])}")
print(f"  Expected new output: {week4_outputs['func3']}")
print(f"  Match? {func3_outputs[-1] == week4_outputs['func3']}")
print(f"  Total points: {len(func3_outputs)}")

# =============================================================================
# FUNCTION 4: APPEND NEW DATA
# =============================================================================
print("\n" + "="*60)
print("FUNCTION 4: APPENDING NEW DATA")
print("="*60)

# APPEND
func4_inputs = np.vstack([func4_inputs, week4_queries['func4']])
func4_outputs = np.append(func4_outputs, week4_outputs['func4'])

# AFTER APPENDING
print(f"\nAFTER:")
print(f"  Inputs shape: {func4_inputs.shape}")  # Now (31, 4)
print(f"  Outputs shape: {func4_outputs.shape}")  # Now (31,)
print(f"  New input point: {func4_inputs[-1]}")
print(f"  New output: {func4_outputs[-1]}")

# VERIFY
print(f"\nVERIFY:")
print(f"  Expected new input: {week4_queries['func4']}")
print(f"  Match? {np.array_equal(func4_inputs[-1], week4_queries['func4'])}")
print(f"  Expected new output: {week4_outputs['func4']}")
print(f"  Match? {func4_outputs[-1] == week4_outputs['func4']}")
print(f"  Total points: {len(func4_outputs)}")

# =============================================================================
# FUNCTION 5: APPEND NEW DATA (THE BIG WINNER!)
# =============================================================================
print("\n" + "="*60)
print("FUNCTION 5: APPENDING NEW DATA")
print("="*60)
# APPEND
func5_inputs = np.vstack([func5_inputs, week4_queries['func5']])
func5_outputs = np.append(func5_outputs, week4_outputs['func5'])

# AFTER APPENDING
print(f"\nAFTER:")
print(f"  Inputs shape: {func5_inputs.shape}")  # Now (16, 4)
print(f"  Outputs shape: {func5_outputs.shape}")  # Now (16,)
print(f"  New input point: {func5_inputs[-1]}")
print(f"  New output: {func5_outputs[-1]:.4f}")
print(f"  New best: {func5_outputs.max():.4f} (was {func5_outputs[:-1].max():.4f})")

# VERIFY
print(f"\nVERIFY:")
print(f"  Expected new input: {week4_queries['func5']}")
print(f"  Match? {np.array_equal(func5_inputs[-1], week4_queries['func5'])}")
print(f"  Expected new output: {week4_outputs['func5']}")
print(f"  Match? {func5_outputs[-1] == week4_outputs['func5']}")
print(f"  Total points: {len(func5_outputs)}")
print(f"  🎉 New best: {func5_outputs.max():.4f}")

# =============================================================================
# FUNCTION 6: APPEND NEW DATA
# =============================================================================
print("\n" + "="*60)
print("FUNCTION 6: APPENDING NEW DATA")
print("="*60)
# APPEND
func6_inputs = np.vstack([func6_inputs, week4_queries['func6']])
func6_outputs = np.append(func6_outputs, week4_outputs['func6'])

# AFTER APPENDING
print(f"\nAFTER:")
print(f"  Inputs shape: {func6_inputs.shape}")  # Now (21, 5)
print(f"  Outputs shape: {func6_outputs.shape}")  # Now (21,)
print(f"  New input point: {func6_inputs[-1]}")
print(f"  New output: {func6_outputs[-1]:.4f}")

# VERIFY
print(f"\nVERIFY:")
print(f"  Expected new input: {week4_queries['func6']}")
print(f"  Match? {np.array_equal(func6_inputs[-1], week4_queries['func6'])}")
print(f"  Expected new output: {week4_outputs['func6']}")
print(f"  Match? {func6_outputs[-1] == week4_outputs['func6']}")
print(f"  Total points: {len(func6_outputs)}")

# =============================================================================
# FUNCTION 7: APPEND NEW DATA
# =============================================================================
print("\n" + "="*60)
print("FUNCTION 7: APPENDING NEW DATA")
print("="*60)
# APPEND
func7_inputs = np.vstack([func7_inputs, week4_queries['func7']])
func7_outputs = np.append(func7_outputs, week4_outputs['func7'])

# AFTER APPENDING
print(f"\nAFTER:")
print(f"  Inputs shape: {func7_inputs.shape}")  # Now (31, 6)
print(f"  Outputs shape: {func7_outputs.shape}")  # Now (31,)
print(f"  New input point: {func7_inputs[-1]}")
print(f"  New output: {func7_outputs[-1]:.4f}")

# VERIFY
print(f"\nVERIFY:")
print(f"  Expected new input: {week4_queries['func7']}")
print(f"  Match? {np.array_equal(func7_inputs[-1], week4_queries['func7'])}")
print(f"  Expected new output: {week4_outputs['func7']}")
print(f"  Match? {func7_outputs[-1] == week4_outputs['func7']}")
print(f"  Total points: {len(func7_outputs)}")

# =============================================================================
# FUNCTION 8: APPEND NEW DATA
# =============================================================================
print("\n" + "="*60)
print("FUNCTION 8: APPENDING NEW DATA")
print("="*60)
# APPEND
func8_inputs = np.vstack([func8_inputs, week4_queries['func8']])
func8_outputs = np.append(func8_outputs, week4_outputs['func8'])

# AFTER APPENDING
print(f"\nAFTER:")
print(f"  Inputs shape: {func8_inputs.shape}")  # Now (41, 8)
print(f"  Outputs shape: {func8_outputs.shape}")  # Now (41,)
print(f"  New input point: {func8_inputs[-1]}")
print(f"  New output: {func8_outputs[-1]:.4f}")

# VERIFY
print(f"\nVERIFY:")
print(f"  Expected new input: {week4_queries['func8']}")
print(f"  Match? {np.array_equal(func8_inputs[-1], week4_queries['func8'])}")
print(f"  Expected new output: {week4_outputs['func8']}")
print(f"  Match? {func8_outputs[-1] == week4_outputs['func8']}")
print(f"  Total points: {len(func8_outputs)}")

# Remember to change the week numbers in the paths below.

# Function 1
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_1\\updated_inputs.npy', func1_inputs)
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_1\\updated_outputs.npy', func1_outputs)

# Function 2
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_2\\updated_inputs.npy', func2_inputs)
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_2\\updated_outputs.npy', func2_outputs)

# Function 3
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_3\\updated_inputs.npy', func3_inputs)
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_3\\updated_outputs.npy', func3_outputs)

# Function 4
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_4\\updated_inputs.npy', func4_inputs)
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_4\\updated_outputs.npy', func4_outputs)

# Function 5
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_5\\updated_inputs.npy', func5_inputs)
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_5\\updated_outputs.npy', func5_outputs)

# Function 6
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_6\\updated_inputs.npy', func6_inputs)
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_6\\updated_outputs.npy', func6_outputs)

# Function 7
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_7\\updated_inputs.npy', func7_inputs)
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_7\\updated_outputs.npy', func7_outputs)

# Function 8
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_8\\updated_inputs.npy', func8_inputs)
np.save('C:\\Users\\hilto\\OneDrive\\Desktop\\Improved RA_12_1\\Data\\Week_4\\function_8\\updated_outputs.npy', func8_outputs)



# =============================================================================
# End of Appending New Data And Verifying
# =============================================================================

"""






# Create a grid of test points (30x30 = 900 points in 2D)
x1 = np.linspace(0, 1, 30)
x2 = np.linspace(0, 1, 30)
X1, X2 = np.meshgrid(x1, x2)
X_test = np.column_stack([X1.ravel(), X2.ravel()])

print("="*60)
print("FITTING GP FOR EACH FUNCTION")
print("="*60)

# Fit Gaussian Process
# Function 1: 2D - RBF kernel
kernel1 = ConstantKernel(1.0) * RBF(length_scale=0.3) + WhiteKernel(noise_level=0.01)  # Using RBF for better flexibility
gp1 = GaussianProcessRegressor(kernel=kernel1, alpha=1e-6, n_restarts_optimizer=10)
gp1.fit(func1_inputs, func1_outputs)
print("✅ func1 fitted (2D, RBF length_scale=0.3)")

# Function 2: 2D - RBF kernel (maybe different length_scale)
kernel2 = ConstantKernel(1.0) * RBF(length_scale=0.2)  # Different length_scale
gp2 = GaussianProcessRegressor(kernel=kernel2, alpha=1e-6, n_restarts_optimizer=10)
gp2.fit(func2_inputs, func2_outputs)
print("✅ func2 fitted (2D, RBF length_scale=0.2)")

# Function 3: 3D - Matern kernel (better for higher dimensions)
kernel3 = ConstantKernel(1.0) * Matern(length_scale=0.1, nu=2.5)
gp3 = GaussianProcessRegressor(kernel=kernel3, alpha=1e-6, n_restarts_optimizer=10)
gp3.fit(func3_inputs, func3_outputs)
print("✅ func3 fitted (3D, Matern nu=2.5)")

# Function 4: 4D - Matern kernel
kernel4 = ConstantKernel(1.0) * Matern(length_scale=0.1, nu=2.5)
gp4 = GaussianProcessRegressor(kernel=kernel4, alpha=1e-6, n_restarts_optimizer=10)
gp4.fit(func4_inputs, func4_outputs)
print("✅ func4 fitted (4D, Matern nu=2.5)")

# Function 5: 4D - Different kernel (maybe longer length_scale)
kernel5 = ConstantKernel(1.0) * Matern(length_scale=0.2, nu=1.5)  # More flexible
gp5 = GaussianProcessRegressor(kernel=kernel5, alpha=1e-6, n_restarts_optimizer=10)
gp5.fit(func5_inputs, func5_outputs)
print("✅ func5 fitted (4D, Matern nu=1.5, length_scale=0.2)")

# Function 6: 5D - Matern with nu=1.5 (allows more roughness)
kernel6 = ConstantKernel(1.0) * Matern(length_scale=0.1, nu=1.5)
gp6 = GaussianProcessRegressor(kernel=kernel6, alpha=1e-6, n_restarts_optimizer=10)
gp6.fit(func6_inputs, func6_outputs)
print("✅ func6 fitted (5D, Matern nu=1.5)")

# Function 7: 6D - Matern with nu=1.5
kernel7 = ConstantKernel(1.0) * Matern(length_scale=0.15, nu=1.5)
gp7 = GaussianProcessRegressor(kernel=kernel7, alpha=1e-6, n_restarts_optimizer=10)
gp7.fit(func7_inputs, func7_outputs)
print("✅ func7 fitted (6D, Matern nu=1.5, length_scale=0.15)")

# Function 8: 8D - Matern with nu=1.5 (higher exploration)
kernel8 = ConstantKernel(1.0) * Matern(length_scale=0.2, nu=1.5)
gp8 = GaussianProcessRegressor(kernel=kernel8, alpha=1e-6, n_restarts_optimizer=10)
gp8.fit(func8_inputs, func8_outputs)
print("✅ func8 fitted (8D, Matern nu=1.5, length_scale=0.2)")


print("="*60)
print("MAKING PREDICTIONS FOR EACH FUNCTION")
print("="*60)

print("\n" + "="*60)
print("FUNCTION 1: MAKING PREDICTIONS")
print("="*60)

# Generate candidate points (10000 random points in 2D)
candidates_f1 = np.random.random((10000, 2))
# Make predictions using gp1
mean_f1, std_f1 = gp1.predict(candidates_f1, return_std=True)
print(f"Predictions for Function 1:")
print(f"  Mean range: [{mean_f1.min():.4f}, {mean_f1.max():.4f}]")
print(f"  Std range: [{std_f1.min():.4f}, {std_f1.max():.4f}]")
# Find best prediction (highest mean)
best_idx_f1 = np.argmax(mean_f1)
best_candidate_f1 = candidates_f1[best_idx_f1]
print(f"  Best predicted point: {best_candidate_f1}")
print(f"  Best predicted mean: {mean_f1[best_idx_f1]:.4f}")

# =============================================================================
# FUNCTION 2: PREDICTIONS (2D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 2: MAKING PREDICTIONS")
print("="*60)

candidates_f2 = np.random.random((10000, 2))
mean_f2, std_f2 = gp2.predict(candidates_f2, return_std=True)
print(f"Predictions for Function 2:")
print(f"  Mean range: [{mean_f2.min():.4f}, {mean_f2.max():.4f}]")
print(f"  Std range: [{std_f2.min():.4f}, {std_f2.max():.4f}]")
best_idx_f2 = np.argmax(mean_f2)
best_candidate_f2 = candidates_f2[best_idx_f2]
print(f"  Best predicted point: {best_candidate_f2}")
print(f"  Best predicted mean: {mean_f2[best_idx_f2]:.4f}")

# =============================================================================
# FUNCTION 3: PREDICTIONS (3D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 3: MAKING PREDICTIONS")
print("="*60)

candidates_f3 = np.random.random((10000, 3))
mean_f3, std_f3 = gp3.predict(candidates_f3, return_std=True)
print(f"Predictions for Function 3:")
print(f"  Mean range: [{mean_f3.min():.4f}, {mean_f3.max():.4f}]")
print(f"  Std range: [{std_f3.min():.4f}, {std_f3.max():.4f}]")
best_idx_f3 = np.argmax(mean_f3)
best_candidate_f3 = candidates_f3[best_idx_f3]
print(f"  Best predicted point: {best_candidate_f3}")
print(f"  Best predicted mean: {mean_f3[best_idx_f3]:.4f}")

# =============================================================================
# FUNCTION 4: PREDICTIONS (4D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 4: MAKING PREDICTIONS")
print("="*60)

candidates_f4 = np.random.random((10000, 4))
mean_f4, std_f4 = gp4.predict(candidates_f4, return_std=True)
print(f"Predictions for Function 4:")
print(f"  Mean range: [{mean_f4.min():.4f}, {mean_f4.max():.4f}]")
print(f"  Std range: [{std_f4.min():.4f}, {std_f4.max():.4f}]")
best_idx_f4 = np.argmax(mean_f4)
best_candidate_f4 = candidates_f4[best_idx_f4]
print(f"  Best predicted point: {best_candidate_f4}")
print(f"  Best predicted mean: {mean_f4[best_idx_f4]:.4f}")

# =============================================================================
# FUNCTION 5: PREDICTIONS (4D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 5: MAKING PREDICTIONS")
print("="*60)

candidates_f5 = np.random.random((10000, 4))
mean_f5, std_f5 = gp5.predict(candidates_f5, return_std=True)
print(f"Predictions for Function 5:")
print(f"  Mean range: [{mean_f5.min():.4f}, {mean_f5.max():.4f}]")
print(f"  Std range: [{std_f5.min():.4f}, {std_f5.max():.4f}]")
best_idx_f5 = np.argmax(mean_f5)
best_candidate_f5 = candidates_f5[best_idx_f5]
print(f"  Best predicted point: {best_candidate_f5}")
print(f"  Best predicted mean: {mean_f5[best_idx_f5]:.4f}")

# =============================================================================
# FUNCTION 6: PREDICTIONS (5D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 6: MAKING PREDICTIONS")
print("="*60)

candidates_f6 = np.random.random((10000, 5))
mean_f6, std_f6 = gp6.predict(candidates_f6, return_std=True)

print(f"Predictions for Function 6:")
print(f"  Mean range: [{mean_f6.min():.4f}, {mean_f6.max():.4f}]")
print(f"  Std range: [{std_f6.min():.4f}, {std_f6.max():.4f}]")

best_idx_f6 = np.argmax(mean_f6)
best_candidate_f6 = candidates_f6[best_idx_f6]
print(f"  Best predicted point: {best_candidate_f6}")
print(f"  Best predicted mean: {mean_f6[best_idx_f6]:.4f}")

# =============================================================================
# FUNCTION 7: PREDICTIONS (6D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 7: MAKING PREDICTIONS")
print("="*60)

candidates_f7 = np.random.random((10000, 6))
mean_f7, std_f7 = gp7.predict(candidates_f7, return_std=True)

print(f"Predictions for Function 7:")
print(f"  Mean range: [{mean_f7.min():.4f}, {mean_f7.max():.4f}]")
print(f"  Std range: [{std_f7.min():.4f}, {std_f7.max():.4f}]")

best_idx_f7 = np.argmax(mean_f7)
best_candidate_f7 = candidates_f7[best_idx_f7]
print(f"  Best predicted point: {best_candidate_f7}")
print(f"  Best predicted mean: {mean_f7[best_idx_f7]:.4f}")

# =============================================================================
# FUNCTION 8: PREDICTIONS (8D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 8: MAKING PREDICTIONS")
print("="*60)

candidates_f8 = np.random.random((10000, 8))
mean_f8, std_f8 = gp8.predict(candidates_f8, return_std=True)

print(f"Predictions for Function 8:")
print(f"  Mean range: [{mean_f8.min():.4f}, {mean_f8.max():.4f}]")
print(f"  Std range: [{std_f8.min():.4f}, {std_f8.max():.4f}]")

best_idx_f8 = np.argmax(mean_f8)
best_candidate_f8 = candidates_f8[best_idx_f8]
print(f"  Best predicted point: {best_candidate_f8}")
print(f"  Best predicted mean: {mean_f8[best_idx_f8]:.4f}")


# =============================================================================
# VISUALIZE FUNCTION 1 PREDICTIONS
# =============================================================================

print("\n" + "="*60)
print("VISUALIZING FUNCTION 1 PREDICTIONS")
print("="*60)

# Get predictions on grid
mu, sigma = gp1.predict(X_test, return_std=True)
mu_grid = mu.reshape(30, 30)
sigma_grid = sigma.reshape(30, 30)

# Plot 1: Mean Prediction
fig, ax = plot_2d_function(X1, X2, mu_grid, title="Function 1: GP Mean Prediction")

# Add training points
ax.scatter(func1_inputs[:, 0], func1_inputs[:, 1], 
           c=func1_outputs, s=80, edgecolors='black', 
           cmap='viridis', vmin=func1_outputs.min(), vmax=func1_outputs.max())

# Highlight best point
best_idx = np.argmax(func1_outputs)
ax.scatter(func1_inputs[best_idx, 0], func1_inputs[best_idx, 1],
           color='red', s=200, marker='*', label='Best observed')
ax.legend()
plt.show()

# Plot 2: Uncertainty
fig, ax = plot_2d_function(X1, X2, sigma_grid, title="Function 1: Prediction Uncertainty")

# Add training points
ax.scatter(func1_inputs[:, 0], func1_inputs[:, 1], 
           s=80, edgecolors='black', facecolors='none')

# Highlight best point
ax.scatter(func1_inputs[best_idx, 0], func1_inputs[best_idx, 1],
           color='red', s=200, marker='*', label='Best observed')
ax.legend()
plt.show()

# =============================================================================
# VISUALIZE FUNCTION 2 PREDICTIONS
# =============================================================================

print("\n" + "="*60)
print("VISUALIZING FUNCTION 2 PREDICTIONS")
print("="*60)

mu, sigma = gp2.predict(X_test, return_std=True)
mu_grid = mu.reshape(30, 30)
sigma_grid = sigma.reshape(30, 30)

fig, ax = plot_2d_function(X1, X2, mu_grid, title="Function 2: GP Mean Prediction")

# Add training points
ax.scatter(func2_inputs[:, 0], func2_inputs[:, 1], 
           c=func2_outputs, s=80, edgecolors='black', 
           cmap='viridis', vmin=func2_outputs.min(), vmax=func2_outputs.max())

# Highlight best point
best_idx = np.argmax(func2_outputs)
ax.scatter(func2_inputs[best_idx, 0], func2_inputs[best_idx, 1],
           color='red', s=200, marker='*', label='Best observed')
ax.legend()
plt.show()

# Plot 2: Uncertainty using your function
fig, ax = plot_2d_function(X1, X2, sigma_grid, title="Function 2: Prediction Uncertainty")

# Add training points
ax.scatter(func2_inputs[:, 0], func2_inputs[:, 1], 
           s=80, edgecolors='black', facecolors='none')

# Highlight best point
ax.scatter(func2_inputs[best_idx, 0], func2_inputs[best_idx, 1],
           color='red', s=200, marker='*', label='Best observed')
ax.legend()
plt.show()

# =============================================================================
# FUNCTION 1: ACQUISITION (2D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 1: ACQUISITION")
print("="*60)

# Best observed value so far
y_best_1 = func1_outputs.max()

# UCB (kappa=1.5 for 2D)
ucb_1 = upper_confidence_bound(mean_f1, std_f1, kappa=0.1)
best_ucb_idx_1 = np.argmax(ucb_1)
next_point_ucb_1 = candidates_f1[best_ucb_idx_1]

# EI
ei_1 = expected_improvement(mean_f1, std_f1, y_best_1, xi=0.1)
best_ei_idx_1 = np.argmax(ei_1)
next_point_ei_1 = candidates_f1[best_ei_idx_1]

print(f"UCB (κ=0.5):")
print(f"  Next point: {next_point_ucb_1[0]:.6f}-{next_point_ucb_1[1]:.6f}")
print(f"  UCB value: {ucb_1[best_ucb_idx_1]:.4f}")
print(f"  Mean: {mean_f1[best_ucb_idx_1]:.4f}")
print(f"  Std: {std_f1[best_ucb_idx_1]:.4f}")

print(f"\nEI (y_best={y_best_1:.4f}):")
print(f"  Next point: {next_point_ei_1[0]:.6f}-{next_point_ei_1[1]:.6f}")
print(f"  EI value: {ei_1[best_ei_idx_1]:.4f}")
print(f"  Mean: {mean_f1[best_ei_idx_1]:.4f}")
print(f"  Std: {std_f1[best_ei_idx_1]:.4f}")



# =============================================================================
# FUNCTION 2: ACQUISITION (2D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 2: ACQUISITION")
print("="*60)

y_best_2 = func2_outputs.max()

ucb_2 = upper_confidence_bound(mean_f2, std_f2, kappa=2.0)
best_ucb_idx_2 = np.argmax(ucb_2)
next_point_ucb_2 = candidates_f2[best_ucb_idx_2]

ei_2 = expected_improvement(mean_f2, std_f2, y_best_2, xi=0.1)
best_ei_idx_2 = np.argmax(ei_2)
next_point_ei_2 = candidates_f2[best_ei_idx_2]

print(f"UCB (κ=2.0):")
print(f"  Next point: {next_point_ucb_2[0]:.6f}-{next_point_ucb_2[1]:.6f}")
print(f"  UCB value: {ucb_2[best_ucb_idx_2]:.4f}")
print(f"  Mean: {mean_f2[best_ucb_idx_2]:.4f}")
print(f"  Std: {std_f2[best_ucb_idx_2]:.4f}")

print(f"\nEI (y_best={y_best_2:.4f}):")
print(f"  Next point: {next_point_ei_2[0]:.6f}-{next_point_ei_2[1]:.6f}")
print(f"  EI value: {ei_2[best_ei_idx_2]:.4f}")
print(f"  Mean: {mean_f2[best_ei_idx_2]:.4f}")
print(f"  Std: {std_f2[best_ei_idx_2]:.4f}")

# =============================================================================
# FUNCTION 3: ACQUISITION (3D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 3: ACQUISITION")
print("="*60)

y_best_3 = func3_outputs.max()

ucb_3 = upper_confidence_bound(mean_f3, std_f3, kappa=1.5)
best_ucb_idx_3 = np.argmax(ucb_3)
next_point_ucb_3 = candidates_f3[best_ucb_idx_3]

ei_3 = expected_improvement(mean_f3, std_f3, y_best_3, xi=0.01)
best_ei_idx_3 = np.argmax(ei_3)
next_point_ei_3 = candidates_f3[best_ei_idx_3]

print(f"UCB (κ=1.5):")
print(f"  Next point: {next_point_ucb_3[0]:.6f}-{next_point_ucb_3[1]:.6f}-{next_point_ucb_3[2]:.6f}")
print(f"  UCB value: {ucb_3[best_ucb_idx_3]:.4f}")
print(f"  Mean: {mean_f3[best_ucb_idx_3]:.4f}")
print(f"  Std: {std_f3[best_ucb_idx_3]:.4f}")

print(f"\nEI (y_best={y_best_3:.4f}):")
print(f"  Next point: {next_point_ei_3[0]:.6f}-{next_point_ei_3[1]:.6f}-{next_point_ei_3[2]:.6f}")
print(f"  EI value: {ei_3[best_ei_idx_3]:.4f}")
print(f"  Mean: {mean_f3[best_ei_idx_3]:.4f}")
print(f"  Std: {std_f3[best_ei_idx_3]:.4f}")

# =============================================================================
# FUNCTION 4: ACQUISITION (4D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 4: ACQUISITION")
print("="*60)

y_best_4 = func4_outputs.max()

ucb_4 = upper_confidence_bound(mean_f4, std_f4, kappa=1.5)
best_ucb_idx_4 = np.argmax(ucb_4)
next_point_ucb_4 = candidates_f4[best_ucb_idx_4]

ei_4 = expected_improvement(mean_f4, std_f4, y_best_4, xi=0.01)
best_ei_idx_4 = np.argmax(ei_4)
next_point_ei_4 = candidates_f4[best_ei_idx_4]

print(f"UCB (κ=1.5):")
print(f"  Next point: {next_point_ucb_4[0]:.6f}-{next_point_ucb_4[1]:.6f}-{next_point_ucb_4[2]:.6f}-{next_point_ucb_4[3]:.6f}")
print(f"  UCB value: {ucb_4[best_ucb_idx_4]:.4f}")
print(f"  Mean: {mean_f4[best_ucb_idx_4]:.4f}")
print(f"  Std: {std_f4[best_ucb_idx_4]:.4f}")

print(f"\nEI (y_best={y_best_4:.4f}):")
print(f"  Next point: {next_point_ei_4[0]:.6f}-{next_point_ei_4[1]:.6f}-{next_point_ei_4[2]:.6f}-{next_point_ei_4[3]:.6f}")
print(f"  EI value: {ei_4[best_ei_idx_4]:.4f}")
print(f"  Mean: {mean_f4[best_ei_idx_4]:.4f}")
print(f"  Std: {std_f4[best_ei_idx_4]:.4f}")

# =============================================================================
# FUNCTION 5: ACQUISITION (4D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 5: ACQUISITION")
print("="*60)

y_best_5 = func5_outputs.max()

ucb_5 = upper_confidence_bound(mean_f5, std_f5, kappa=1.5)
best_ucb_idx_5 = np.argmax(ucb_5)
next_point_ucb_5 = candidates_f5[best_ucb_idx_5]

ei_5 = expected_improvement(mean_f5, std_f5, y_best_5, xi=0.01)
best_ei_idx_5 = np.argmax(ei_5)
next_point_ei_5 = candidates_f5[best_ei_idx_5]

print(f"UCB (κ=1.5):")
print(f"  Next point: {next_point_ucb_5[0]:.6f}-{next_point_ucb_5[1]:.6f}-{next_point_ucb_5[2]:.6f}-{next_point_ucb_5[3]:.6f}")
print(f"  UCB value: {ucb_5[best_ucb_idx_5]:.4f}")
print(f"  Mean: {mean_f5[best_ucb_idx_5]:.4f}")
print(f"  Std: {std_f5[best_ucb_idx_5]:.4f}")

print(f"\nEI (y_best={y_best_5:.4f}):")
print(f"  Next point: {next_point_ei_5[0]:.6f}-{next_point_ei_5[1]:.6f}-{next_point_ei_5[2]:.6f}-{next_point_ei_5[3]:.6f}")
print(f"  EI value: {ei_5[best_ei_idx_5]:.4f}")
print(f"  Mean: {mean_f5[best_ei_idx_5]:.4f}")
print(f"  Std: {std_f5[best_ei_idx_5]:.4f}")

# =============================================================================
# FUNCTION 6: ACQUISITION (5D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 6: ACQUISITION")
print("="*60)

y_best_6 = func6_outputs.max()

ucb_6 = upper_confidence_bound(mean_f6, std_f6, kappa=2.5)
best_ucb_idx_6 = np.argmax(ucb_6)
next_point_ucb_6 = candidates_f6[best_ucb_idx_6]

ei_6 = expected_improvement(mean_f6, std_f6, y_best_6, xi=0.01)
best_ei_idx_6 = np.argmax(ei_6)
next_point_ei_6 = candidates_f6[best_ei_idx_6]

print(f"UCB (κ=2.5):")
print(f"  Next point: {next_point_ucb_6[0]:.6f}-{next_point_ucb_6[1]:.6f}-{next_point_ucb_6[2]:.6f}-{next_point_ucb_6[3]:.6f}-{next_point_ucb_6[4]:.6f}")
print(f"  UCB value: {ucb_6[best_ucb_idx_6]:.4f}")
print(f"  Mean: {mean_f6[best_ucb_idx_6]:.4f}")
print(f"  Std: {std_f6[best_ucb_idx_6]:.4f}")

print(f"\nEI (y_best={y_best_6:.4f}):")
print(f"  Next point: {next_point_ei_6[0]:.6f}-{next_point_ei_6[1]:.6f}-{next_point_ei_6[2]:.6f}-{next_point_ei_6[3]:.6f}-{next_point_ei_6[4]:.6f}")
print(f"  EI value: {ei_6[best_ei_idx_6]:.4f}")
print(f"  Mean: {mean_f6[best_ei_idx_6]:.4f}")
print(f"  Std: {std_f6[best_ei_idx_6]:.4f}")

# =============================================================================
# FUNCTION 7: ACQUISITION (6D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 7: ACQUISITION")
print("="*60)

y_best_7 = func7_outputs.max()

ucb_7 = upper_confidence_bound(mean_f7, std_f7, kappa=1.7)
best_ucb_idx_7 = np.argmax(ucb_7)
next_point_ucb_7 = candidates_f7[best_ucb_idx_7]

ei_7 = expected_improvement(mean_f7, std_f7, y_best_7, xi=0.01)
best_ei_idx_7 = np.argmax(ei_7)
next_point_ei_7 = candidates_f7[best_ei_idx_7]

print(f"UCB (κ=1.7):")
print(f"  Next point: {next_point_ucb_7[0]:.6f}-{next_point_ucb_7[1]:.6f}-{next_point_ucb_7[2]:.6f}-{next_point_ucb_7[3]:.6f}-{next_point_ucb_7[4]:.6f}-{next_point_ucb_7[5]:.6f}")
print(f"  UCB value: {ucb_7[best_ucb_idx_7]:.4f}")
print(f"  Mean: {mean_f7[best_ucb_idx_7]:.4f}")
print(f"  Std: {std_f7[best_ucb_idx_7]:.4f}")

print(f"\nEI (y_best={y_best_7:.4f}):")
print(f"  Next point: {next_point_ei_7[0]:.6f}-{next_point_ei_7[1]:.6f}-{next_point_ei_7[2]:.6f}-{next_point_ei_7[3]:.6f}-{next_point_ei_7[4]:.6f}-{next_point_ei_7[5]:.6f}")
print(f"  EI value: {ei_7[best_ei_idx_7]:.4f}")
print(f"  Mean: {mean_f7[best_ei_idx_7]:.4f}")
print(f"  Std: {std_f7[best_ei_idx_7]:.4f}")

# =============================================================================
# FUNCTION 8: ACQUISITION (8D)
# =============================================================================

print("\n" + "="*60)
print("FUNCTION 8: ACQUISITION")
print("="*60)

y_best_8 = func8_outputs.max()

ucb_8 = upper_confidence_bound(mean_f8, std_f8, kappa=3.0)
best_ucb_idx_8 = np.argmax(ucb_8)
next_point_ucb_8 = candidates_f8[best_ucb_idx_8]

ei_8 = expected_improvement(mean_f8, std_f8, y_best_8, xi=0.02)
best_ei_idx_8 = np.argmax(ei_8)
next_point_ei_8 = candidates_f8[best_ei_idx_8]

print(f"UCB (κ=3.0):")
print(f"  Next point: {next_point_ucb_8[0]:.6f}-{next_point_ucb_8[1]:.6f}-{next_point_ucb_8[2]:.6f}-{next_point_ucb_8[3]:.6f}-{next_point_ucb_8[4]:.6f}-{next_point_ucb_8[5]:.6f}-{next_point_ucb_8[6]:.6f}-{next_point_ucb_8[7]:.6f}")
print(f"  UCB value: {ucb_8[best_ucb_idx_8]:.4f}")
print(f"  Mean: {mean_f8[best_ucb_idx_8]:.4f}")
print(f"  Std: {std_f8[best_ucb_idx_8]:.4f}")

print(f"\nEI (y_best={y_best_8:.4f}):")
print(f"  Next point: {next_point_ei_8[0]:.6f}-{next_point_ei_8[1]:.6f}-{next_point_ei_8[2]:.6f}-{next_point_ei_8[3]:.6f}-{next_point_ei_8[4]:.6f}-{next_point_ei_8[5]:.6f}-{next_point_ei_8[6]:.6f}-{next_point_ei_8[7]:.6f}")
print(f"  EI value: {ei_8[best_ei_idx_8]:.4f}")
print(f"  Mean: {mean_f8[best_ei_idx_8]:.4f}")
print(f"  Std: {std_f8[best_ei_idx_8]:.4f}")

# =============================================================================
# VISUALIZE ACQUISITION FOR FUNCTION 1
# =============================================================================
print("\n" + "="*60)
print("VISUALIZING ACQUISITION: FUNCTION 1")
print("="*60)

# Create test grid
x1 = np.linspace(0, 1, 30)
x2 = np.linspace(0, 1, 30)
X1, X2 = np.meshgrid(x1, x2)
X_test = np.column_stack([X1.ravel(), X2.ravel()])

# Get GP predictions on grid
mu_1, sigma_1 = gp1.predict(X_test, return_std=True)
mu_grid_1 = mu_1.reshape(30, 30)
sigma_grid_1 = sigma_1.reshape(30, 30)

# UCB on grid
ucb_grid_1 = mu_grid_1 + 1.5 * sigma_grid_1

# Plot UCB
fig, ax = plot_2d_function(X1, X2, ucb_grid_1, title="Function 1: UCB Acquisition (κ=1.5)")
ax.scatter(func1_inputs[:, 0], func1_inputs[:, 1], 
           c='white', s=80, edgecolors='black', alpha=0.5)
ax.scatter(next_point_ucb_1[0], next_point_ucb_1[1], 
           color='red', s=300, marker='*', label='Next query (UCB)')
ax.legend()
plt.show()

# EI on grid
ei_grid_1 = np.zeros_like(X1)
for i in range(30):
    for j in range(30):
        point = np.array([[X1[i, j], X2[i, j]]])
        mu, sigma = gp1.predict(point, return_std=True)
        ei_grid_1[i, j] = expected_improvement(mu, sigma, y_best_1, xi=0.01)

# Plot EI
fig, ax = plot_2d_function(X1, X2, ei_grid_1, title=f"Function 1: Expected Improvement (y_best={y_best_1:.4f})")
ax.scatter(func1_inputs[:, 0], func1_inputs[:, 1], 
           c='white', s=80, edgecolors='black', alpha=0.5)
ax.scatter(next_point_ei_1[0], next_point_ei_1[1], 
           color='red', s=300, marker='*', label='Next query (EI)')
ax.legend()
plt.show()

# =============================================================================
# VISUALIZE ACQUISITION FOR FUNCTION 2
# =============================================================================

print("\n" + "="*60)
print("VISUALIZING ACQUISITION: FUNCTION 2")
print("="*60)

# Get GP predictions on grid
mu_2, sigma_2 = gp2.predict(X_test, return_std=True)
mu_grid_2 = mu_2.reshape(30, 30)
sigma_grid_2 = sigma_2.reshape(30, 30)

# UCB on grid
ucb_grid_2 = mu_grid_2 + 1.5 * sigma_grid_2

# Plot UCB
fig, ax = plot_2d_function(X1, X2, ucb_grid_2, title="Function 2: UCB Acquisition (κ=1.5)")
ax.scatter(func2_inputs[:, 0], func2_inputs[:, 1], 
           c='white', s=80, edgecolors='black', alpha=0.5)
ax.scatter(next_point_ucb_2[0], next_point_ucb_2[1], 
           color='red', s=300, marker='*', label='Next query (UCB)')
ax.legend()
plt.show()

# EI on grid
ei_grid_2 = np.zeros_like(X1)
for i in range(30):
    for j in range(30):
        point = np.array([[X1[i, j], X2[i, j]]])
        mu, sigma = gp2.predict(point, return_std=True)
        ei_grid_2[i, j] = expected_improvement(mu, sigma, y_best_2, xi=0.01)

# Plot EI
fig, ax = plot_2d_function(X1, X2, ei_grid_2, title=f"Function 2: Expected Improvement (y_best={y_best_2:.4f})")
ax.scatter(func2_inputs[:, 0], func2_inputs[:, 1], 
           c='white', s=80, edgecolors='black', alpha=0.5)
ax.scatter(next_point_ei_2[0], next_point_ei_2[1], 
           color='red', s=300, marker='*', label='Next query (EI)')
ax.legend()
plt.show()


