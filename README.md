# Hybrid Active Brownian Particles and Phase Field Simulation

Thi repository contains the source code and postprocessing tools for the simulation of active particles in a phase-separating binary mixture. The model integrates a Cahn-Hilliard (Model B) field with Active Brownian Particles (ABPs).

## Project Overview

The simulation handles the co-evolution of two distinct but coupled systems:
1. Phase Field: A continuous field governed by Model B kinetics to simulate phase separation (spinodal decomposition).
2. Active Particles: Discrete agents following Langevin dynamics with self-propulsion and repulsive interactions.

The coupling logic allows for the study of Motility-Induced Phase Separation (MIPS) and the influence of chemical affinities on droplet formation and growth.

## Installation and Compilation

### Prerequisites
* Fortran Compiler: gfortran (version 9.0+) or Intel ifort.
* Python: Version 3.8+ with NumPy and Matplotlib.
* Build System: GNU Make.

### Compilation
To build the executable, navigate to the project root and use the provided Makefile:

bash
make

This will generate the main.exe binary. To remove compiled objects and module files, use make clean.

## Usage

### 1. Configuration
Simulation parameters (grid size, particle number, active velocity, time step) are managed via the parameters.in file. Ensure this file is present in the execution directory.

### 2. Running the Simulation
Execute the binary directly:

bash
./main.exe

### 3. Checkpointing and Restarts
The engine includes a binary checkpointing system. 
* At defined intervals, the system state is saved to checkpoint.bin.
* On startup, the program automatically searches for this file.
* If found, the simulation resumes from the last saved step.
* To start a new simulation from t=0, ensure no checkpoint.bin exists in the folder.

## Analysis Tools

The Tools/ directory contains Python scripts for post-processing and visualization.

* Snapshots: python3 Tools/analyze_sweep.py generates 2D visualizations of the field and particle positions, including orientation vectors.
* Statistics: python3 Tools/analyze_stats.py processes stats.dat and free_energy.dat to produce dashboards showing energy minimization and domain growth.

## Data Output Structure

The code generates the following outputs for analysis:

| File | Description |
| :--- | :--- |
| field_psi_*.txt | 2D grid data of the phase field concentration. |
| particles_*.txt | Coordinates (x, y) and orientation angles of all particles. |
| free_energy.dat | Time-series of Field, Particle, and Coupling energy components. |
| stats.dat | Characteristic domain size measurements over time. |
| performance.txt | CPU time logs for benchmarking. |

## License

This project is licensed under the MIT License.

## Contact

Javier D. - [javierD92](https://github.com/javierD92)