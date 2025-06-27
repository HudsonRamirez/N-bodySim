# N-Body Simulator

A simple implementation of a gravitational N-body simulator using Leapfrog integration.

## Features

- Pairwise Newtonian gravity
- Leapfrog (symplectic) integrator
- Energy tracking (kinetic, potential, total)
- Basic 2D plotting of trajectories and energies

## Requirements

- Python 3.x
- `numpy`
- `matplotlib`

## Running a Simulation

```python
from nbody import Body, NBodySimulator

# Initialize bodies
planet = Body(0.1, [0.0, 1.0], [1.0, 0.0])
star = Body(1.0, [0.0, 0.0], [0.0, 0.0])
bodies = [planet, star]

# Run simulation
sim = NBodySimulator(bodies, dt=0.1, n_steps=1000)
sim.RunSim()
sim.PlotTrajectories()
sim.PlotEnergies()
