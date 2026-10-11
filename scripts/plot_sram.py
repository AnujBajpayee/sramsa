import numpy as np
import matplotlib.pyplot as plt
import os

# Path to the Ngspice wrdata output file
data_file = os.path.join("..", "results", "sram_data.txt")

# Load data: Ngspice wrdata files are tabular text where columns are [time, sig1_real, sig1_imag, sig2_real, sig2_imag...]
# For real transient analysis, we want columns 0 (time), 1 (cell_Q), 3 (cell_QB), and 5 (WL)
data = np.loadtxt(data_file)

time = data[:, 0] * 1e9  # Convert time to nanoseconds for easier reading
cell_q = data[:, 1]
cell_qb = data[:, 3]
wl = data[:, 5]

# Plotting the waveforms
plt.figure(figsize=(10, 6))

plt.plot(time, cell_q, label="cell_Q", linewidth=2, color="blue")
plt.plot(time, cell_qb, label="cell_QB", linewidth=2, color="orange")
plt.plot(time, wl, label="Wordline (WL)", linewidth=1.5, linestyle="--", color="red")

plt.title("6T SRAM Bitcell Transient Simulation (SKY130)", fontsize=14)
plt.xlabel("Time (ns)", fontsize=12)
plt.ylabel("Voltage (V)", fontsize=12)
plt.grid(True, which="both", linestyle=":", alpha=0.7)
plt.axhline(y=0.9, color="gray", linestyle="-.", alpha=0.5, label="Vdd / 2")
plt.legend(loc="upper right", fontsize=11)
plt.ylim(-0.2, 2.0)

# Save the plot image into the results directory
output_image = os.path.join("..", "results", "sram_waveform.png")
plt.savefig(output_image, dpi=300, bbox_inches="tight")
print(f"Plot successfully saved to {output_image}")

# Show the plot window interactively
plt.show()