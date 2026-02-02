import numpy as np
from scipy import ndimage
from skimage import measure
import matplotlib.pyplot as plt
import os 
from matplotlib.colors import ListedColormap

def get_droplet_labels(psi_field, threshold=0.0):
    # 1. Binary mask (psi < 0 is droplet)
    binary_mask = (psi_field < threshold).astype(int)
    
    # 2. Initial Labeling
    labels, num_features = ndimage.label(binary_mask)
    
    # 3. Handle PBCs
    rows, cols = binary_mask.shape
    for j in range(cols):
        if binary_mask[0, j] and binary_mask[-1, j]:
            labels[labels == labels[-1, j]] = labels[0, j]
    for i in range(rows):
        if binary_mask[i, 0] and binary_mask[i, -1]:
            labels[labels == labels[i, -1]] = labels[i, 0]

    # Relabel to contiguous integers to make coloring easier
    unique_labels = np.unique(labels)
    relabeled = np.zeros_like(labels)
    for new_id, old_id in enumerate(unique_labels):
        if old_id == 0: continue
        relabeled[labels == old_id] = new_id
        
    return relabeled

# --- Data Loading ---
path = "/media/javi/Elements_UB/UB/code2.0/Simulations/active-emulsion_diffusion/data"
file = "field_psi_770000.txt"
data = np.loadtxt(os.path.join(path, file)) 
psi = np.reshape(data[:, 2], (512, 512))

# Get the labels
labeled_field = get_droplet_labels(psi)
num_droplets = np.max(labeled_field)

# --- Generate a Random Colormap ---
# We create a list of random RGB values for each droplet ID
# Setting a seed so the colors are consistent if you run it twice
np.random.seed(42) 
random_colors = np.random.rand(num_droplets + 1, 3)
random_colors[0] = [0, 0, 0] # Set background (ID 0) to Black
custom_cmap = ListedColormap(random_colors)

# --- Plotting ---
plt.figure(figsize=(10, 10))
plt.imshow(labeled_field, cmap=custom_cmap, interpolation='nearest')

# Visual aid: Draw a thin red line to show where the box edges are
plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.3)
plt.axhline(y=255.5, color='r', linestyle='--', alpha=0.3)
plt.axvline(x=0.5, color='r', linestyle='--', alpha=0.3)
plt.axvline(x=255.5, color='r', linestyle='--', alpha=0.3)

plt.title(f"Randomly Colored Droplets (PBC Check)\nFound {num_droplets} droplets")
plt.axis('off')
plt.tight_layout()
plt.show()

# Verification print
areas = [p.area for p in measure.regionprops(labeled_field)]
print(f"Total Droplets: {len(areas)}")