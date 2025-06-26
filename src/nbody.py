import numpy as np
import matplotlib.pyplot as plt

G = 1.0 # Gravitational constant (1 for simplicity)

# Masses
m1 = 1.0 # Star
m2 = 0.001 # Planet

# Positions: [x, y]
x1 = np.array([0.0, 0.0])
x2 = np.array([1.0, 0.0])

# Velocities: [vx, vy]
v1 = np.array([0.0, 0.0])
v2 = np.array([0.5, 1.0])

# Gravitation Acceleration Funciton:
# Input: position of star, position of planet, mass of planet
# Retuns: Acceleration vector d/t^2 acting on pos1 from pos2
def acceleration(pos1, pos2, m2):
    r = pos2 - pos1
    dist = np.linalg.norm(r)

    return G * m2 * r / dist**3


# Precompute initial accelerations for leapfrog integration
a1 = acceleration(x1, x2, m2)
a2 = acceleration(x2, x1, m1)

# Time setup
dt = 0.01
n_steps = 10000

# Arrays to store positions
positions1 = []
positions2 = []

# Arrays to store energies
KEs = []
PEs = []
Es = []

for _ in range(n_steps):
    # Records positions
    positions1.append(x1.copy())
    positions2.append(x2.copy())

    # Half-step velocity update
    v1 += 0.5 * a1 * dt
    v2 += 0.5 * a2 * dt

    # Full step position update
    x1 += v1 * dt
    x2 += v2 * dt

    # Compute accelerations at new position
    a1 = acceleration(x1, x2, m2)
    a2 = acceleration(x2, x1, m1)

    # Complete velocity step
    v1 += 0.5 * a1 * dt
    v2 += 0.5 * a2 * dt

    # Compute kinetic energies
    KE1 = 0.5 * m1 * np.linalg.norm(v1)**2
    KE2 = 0.5 * m2 * np.linalg.norm(v2)**2
    KE_total = KE1 + KE2

    # Compute potential energy
    r = np.linalg.norm(x2 - x1)
    PE = -G * m1 * m2 / r

    # Total energy
    E = KE_total + PE

    # Save to lists
    KEs.append(KE_total)
    PEs.append(PE)
    Es.append(E)

    

# Plot
positions1 = np.array(positions1)
positions2 = np.array(positions2)

plt.plot(positions1[:, 0], positions1[:, 1], label='Star')
plt.plot(positions2[:, 0], positions2[:, 1], label='Planet')
plt.xlabel("x")
plt.ylabel("y")
plt.gca().set_aspect('equal')
plt.legend()
plt.title("2-Body Orbit Simulation")
plt.show()

plt.plot(Es, label='Total Energy')
plt.plot(KEs, label='Kinetic')
plt.plot(PEs, label='Potential')
plt.title("Energy vs Time")
plt.xlabel("Step")
plt.ylabel("Energy")
plt.legend()
plt.grid(True)
plt.show()