import numpy as np
import matplotlib.pyplot as plt
import glob
import re
import sys
import os

# --- Command Line Argument Handling ---
data_path = sys.argv[1] if len(sys.argv) > 1 else "."

# --- Helper: Infer Params from parameters.in ---
def get_params(path):
    param_file = os.path.join(path, "parameters.in")
    # Defaults
    lx, ly = 128, 128 
    tau, u, dt = 0.35, 0.5, 0.001 
    
    if os.path.exists(param_file):
        try:
            with open(param_file, 'r') as f:
                lines = f.readlines()
                # 1. Lx, Ly (Line 1)
                lx_ly = lines[0].split('!')[0].split()
                lx, ly = int(float(lx_ly[0])), int(float(lx_ly[1]))
                
                # 2. dt (usually line 6 in your format)
                # We search for the "dt" comment to be safe
                for line in lines:
                    val_part = line.split('!')[0].strip()
                    comment_part = line.split('!')[-1].lower() if '!' in line else ""
                    
                    if "dt" in comment_part:
                        dt = float(val_part)
                    if "field params" in comment_part:
                        # Format: M kappa tau u
                        parts = val_part.split()
                        tau = float(parts[2])
                        u = float(parts[3])
                
                print(f"Params Inferred: Grid={lx}x{ly}, dt={dt}, tau={tau}, u={u}")
        except Exception as e:
            print(f"Warning: Error parsing params ({e}). Using defaults.")
    return lx, ly, tau, u, dt

# Extract all needed values
LX, LY, TAU, U, DT = get_params(data_path)
PSI_EQ = np.sqrt(TAU / U)
V_MIN, V_MAX = -1.1, 1.1 # Adjusted to show slightly beyond equilibrium

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# Find files in the targeted directory
p_files = sorted(glob.glob(os.path.join(data_path, 'particles_*.txt')), key=natural_sort_key)
f_files = sorted(glob.glob(os.path.join(data_path, 'field_psi_*.txt')), key=natural_sort_key)

if not p_files or not f_files:
    print(f"Error: No .dat files found in directory: {os.path.abspath(data_path)}")
    sys.exit(1)

# --- Setup Plotting (Colorblind Friendly) ---
plt.ion() 
fig, ax = plt.subplots(figsize=(8, 7))

# Initial Load
p_data = np.loadtxt(p_files[0])
f_data = np.loadtxt(f_files[0])

# Reshape logic
def reshape_field(data, lx, ly):
    if data.ndim == 1:
        return data.reshape((ly, lx))
    elif data.shape[1] == 3:
        return data[:, 2].reshape((ly, lx))
    return data

psi = reshape_field(f_data, LX, LY)

# Plotting with inferred dimensions
im = ax.imshow(psi, extent=[0, LX, 0, LY], origin='lower', 
               cmap='RdBu_r', vmin=V_MIN, vmax=V_MAX,
               interpolation='bilinear')

# Check if p_data has content before initializing scatter/quiver
if p_data.size > 0:
    pts = ax.scatter(p_data[:, 0], p_data[:, 1], c='#F0E442', 
                     edgecolors='black', s=20, zorder=3)
    u, v = np.cos(p_data[:, 2]), np.sin(p_data[:, 2])
    qvr = ax.quiver(p_data[:, 0], p_data[:, 1], u, v, color='white', 
                    pivot='tip', scale=60, width=0.003, zorder=4)
else:
    # Initialize empty objects so the loop doesn't fail
    pts = ax.scatter([], [], c='#F0E442', edgecolors='black', s=20, zorder=3)
    qvr = ax.quiver([], [], [], [], color='white', pivot='tip', zorder=4)

ax.set_title(f"Visualizing: {os.path.abspath(data_path)}")
plt.colorbar(im, ax=ax, label='Field $\psi$')

# --- Animation Loop ---
for i in range(len(p_files)):
    try:
        p_curr = np.loadtxt(p_files[i])
    except Exception:
        p_curr = np.array([]) # Handle read errors as empty
        
    f_curr = np.loadtxt(f_files[i])
    
    # Update Field (Always happens)
    psi = reshape_field(f_curr, LX, LY) / PSI_EQ
    im.set_array(psi)
    
    # Update Particles only if file is not empty
    if p_curr.size > 0 and p_curr.ndim > 0:
        pts.set_visible(True)
        qvr.set_visible(True)
        
        pts.set_offsets(p_curr[:, :2])
        
        u_new, v_new = np.cos(p_curr[:, 2]), np.sin(p_curr[:, 2])
        qvr.set_offsets(p_curr[:, :2])
        qvr.set_UVC(u_new, v_new)
    else:
        # Hide particle elements if no data is present
        pts.set_visible(False)
        qvr.set_visible(False)
    
    # Update Text/Metadata
    step_num = int(re.findall(r'\d+', os.path.basename(p_files[i]))[0])
    physical_time = step_num * DT
    ax.set_xlabel(f"Frame: {i} | Step: {step_num} | Time: {physical_time:.2f}")
    
    plt.draw()
    plt.pause(0.01)