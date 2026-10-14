import numpy as np
import matplotlib.pyplot as plt
import os

def parse_ngspice_raw(filepath):
    """
    Robust parser for Ngspice ASCII .raw files.
    Handles multi-line wrapped values, header metadata, 
    and returns a time array and a dictionary of vector data.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Raw file not found: {filepath}")

    with open(filepath, 'r') as f:
        lines = f.readlines()

    variables = []
    data_start = False
    raw_data_lines = []
    num_variables = 0
    num_points = 0

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith("No. Variables:"):
            num_variables = int(line.split(":")[-1].strip())
        elif line.startswith("No. Points:"):
            num_points = int(line.split(":")[-1].strip())
        elif line.startswith("Variables:"):
            i += 1
            for _ in range(num_variables):
                if i < len(lines):
                    parts = lines[i].strip().split()
                    if len(parts) >= 2:
                        variables.append(parts[1].lower())
                    i += 1
            continue
        elif line.startswith("Values:"):
            data_start = True
            i += 1
            continue
        
        if data_start:
            raw_data_lines.append(line)
        i += 1

    # Flatten and parse data points (handling multi-line wrapping)
    flat_values = []
    for line in raw_data_lines:
        parts = line.split()
        for p in parts:
            try:
                flat_values.append(float(p))
            except ValueError:
                continue

    data_matrix = []
    idx = 0
    while idx < len(flat_values):
        if idx + num_variables < len(flat_values):
            point_idx = flat_values[idx]
            time_val = flat_values[idx + 1]
            var_vals = flat_values[idx + 2 : idx + 2 + (num_variables - 1)]
            data_matrix.append([time_val] + var_vals)
            idx += (num_variables + 1)
        else:
            break

    data_array = np.array(data_matrix)
    
    parsed_data = {}
    if data_array.size > 0:
        parsed_data['time'] = data_array[:, 0]
        for v_idx, v_name in enumerate(variables[1:], start=1):
            if v_idx < data_array.shape[1]:
                parsed_data[v_name] = data_array[:, v_idx]

    return parsed_data

def plot_sram_comparative_waveforms():
    nosense_file = "C:/sramsa/results/sram_nosense_output.raw"
    
    print(f"Looking for simulation data at: {nosense_file}")
    
    try:
        data_nosense = parse_ngspice_raw(nosense_file)
    except FileNotFoundError:
        print(f"Error: Could not find raw file at {nosense_file}.")
        return

    # Setup the multi-panel presentation figure
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # --- Subplot 1: Bitline Comparison ---
    axes[0].set_title("6T SRAM Read Path: Full-Rail Discharge (Without Sense Amp)", fontsize=13, fontweight='bold')
    if 'time' in data_nosense:
        t = data_nosense['time'] * 1e9  # convert to nanoseconds
        
        # Plot BL and BLB dynamically matching available keys
        for key in data_nosense.keys():
            if 'blb' in key:
                axes[0].plot(t, data_nosense[key], label='BLB (Bar)', color='darkorange', linestyle='--', linewidth=1.2)
            elif 'bl' in key:
                axes[0].plot(t, data_nosense[key], label='BL (Full-Rail Drop)', color='red', linewidth=1.5)
            elif 'wl' in key:
                axes[0].plot(t, data_nosense[key] * 0.9, label='WL (Scaled x0.9)', color='black', alpha=0.7)
            
    axes[0].set_ylabel("Voltage (V)", fontsize=11)
    axes[0].grid(True, linestyle='--', alpha=0.6)
    axes[0].legend(loc='upper right')

    # --- Subplot 2: Internal Storage Node Behavior (Dynamic Q search) ---
    axes[1].set_title("Internal Cell Node Response (Q / QB)", fontsize=13, fontweight='bold')
    if 'time' in data_nosense:
        plotted_q = False
        for key in data_nosense.keys():
            if 'q' in key and 'bl' not in key:  # matches q, xcell.q, q_int etc.
                axes[1].plot(t, data_nosense[key], label=f'Storage Node ({key})', color='blue', linewidth=1.5)
                plotted_q = True
        
        if not plotted_q:
            # Fallback if no explicit q found
            axes[1].plot(t, np.zeros_like(t), label='No Q Node Found', color='gray', linestyle=':')

    axes[1].set_xlabel("Time (ns)", fontsize=11)
    axes[1].set_ylabel("Voltage (V)", fontsize=11)
    axes[1].grid(True, linestyle='--', alpha=0.6)
    axes[1].legend(loc='upper right')

    plt.tight_layout()
    
    # Save output plot directly into results folder as requested
    os.makedirs("C:/sramsa/results", exist_ok=True)
    output_path = "C:/sramsa/results/sram_nosense_comparison.png"
    plt.savefig(output_path, dpi=300)
    print(f"Comparative waveform plot successfully generated and saved to {output_path}!")
    plt.show()

if __name__ == "__main__":
    plot_sram_comparative_waveforms()