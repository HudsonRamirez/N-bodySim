"""
N-Body Simulator (2D)
Hudson W. Ramirez

Simulates gravitational interaction between bodies using 
a leapfrog integration method.

Includes trajectory and energy plotting.

"""

import numpy as np
import matplotlib.pyplot as plt

G = 1.0 # Gravitational constant (1 for simplicity)

# Time setup
dt = 0.0001
n_steps = 1000

# Gravitation Acceleration Funciton:
# Input: position of star, position of planet, mass of planet
# Returns: Acceleration vector d/t^2 acting on pos1 from pos2
def acceleration(pos1, pos2, m2):
    r = pos2 - pos1
    dist = np.linalg.norm(r)

    return G * m2 * r / dist**3

# Body class:
# Input: mass and position vector
class Body:
    def __init__(self, m, x, v):
        self.m = m
        self.x = np.array(x, dtype = float)
        self.v = np.array(v, dtype = float)
        self.a = np.zeros(2)
        self.positions = [x]
    



# N-Body Simulator Class:
# Input: list of body class objects
class NBodySimulator:
    def __init__(self, bodies, dt, n_steps):
        self.bodies = bodies
        self.dt = dt
        self.n_steps = n_steps

    KEs = []
    PEs = []
    Es = []
    
    # Pairwise acceleration computation
    def compute_accelerations(self):
        for body1 in self.bodies:
            net_acc = np.zeros(2)
            for body2 in self.bodies:
                if body1 is not body2:
                    acc = acceleration(body1.x, body2.x, body2.m)
                    net_acc += acc
            body1.a = net_acc
    
    def RunSim(self):
        # Compute for n steps
        for _ in range(n_steps):
            
            # Loop through all bodies
            for body in self.bodies:
                # Half-step velocity update
                body.v += 0.5 * body.a * self.dt
                # Full step position update
                body.x += body.v * self.dt
                body.positions.append(body.x.copy())

            # Compute accelerations at new position
            self.compute_accelerations()

            stepKEs = []
            # Loop through all bodies again
            for body in self.bodies:
                # Complete velocity step
                body.v += 0.5 * body.a * self.dt

                # Compute kinetic energy
                KE = 0.5 * body.m * np.linalg.norm(body.v)**2
                stepKEs.append(KE)

            # Compute pairwise potential energy one per unique pair
            stepPE = 0.0
            for i, body1 in enumerate(self.bodies):
                for j in range(i+1, len(self.bodies)):
                    body2 = self.bodies[j]
                    r = np.linalg.norm(body2.x - body1.x)
                    stepPE += -G * body1.m * body2.m / r
                
                # Sum all energies across bodies
                KE = sum(stepKEs)
                PE = stepPE
                E = KE + PE
                
                # Save to lists
                self.KEs.append(KE)
                self.PEs.append(PE)
                self.Es.append(E)

    def PlotTrajectories(self):
        for i, body in enumerate(self.bodies):
            positions = np.array(body.positions)
            plt.plot(positions[:, 0], positions[:, 1], label=f'Body {i}')
        
        plt.xlabel("x")
        plt.ylabel("y")
        plt.gca().set_aspect('equal')
        plt.legend()
        plt.title("2-Body Orbit Simulation")
        plt.show()
    
    def PlotEnergies(self):
        plt.plot(self.Es, label='Total Energy')
        plt.plot(self.KEs, label='Kinetic')
        plt.plot(self.PEs, label='Potential')
        plt.title("Energy vs Time")
        plt.xlabel("Step")
        plt.ylabel("Energy")
        plt.legend()
        plt.grid(True)
        plt.show()


Planet = Body(0.1, [0.0, 1.0], [1.0, 0.0])
Star = Body(1.0, [0.0, 0.0], [0.0, 0.0])

bodies = [Planet, Star]

sim = NBodySimulator(bodies, 0.1, 1000)
sim.RunSim()
sim.PlotTrajectories()
sim.PlotEnergies()