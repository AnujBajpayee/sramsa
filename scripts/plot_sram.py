import os
import matplotlib.pyplot as plt
import numpy as np

# Paths
raw_file_path = r"C:\sramsa\results\sram_tran.raw"
output_plot_path = r"C:\sramsa\results\sram_waveforms.png"

def parse_ngspice_raw(filepath):
    """Robust parser for Ngspice ASCII raw files handling multi-line wrapped values."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find raw file at: {filepath}")

    with open(filepath, 'r') as f:
        lines = f.readlines()

    vars_list = []
    data_start = False
    raw_rows = []
    current_row = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith("Variables:"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("Values:"):
                parts = lines[i].strip().split()
                if len(parts) >= 2:
                    vars_list.append(parts[1].lower())
                i += 1
            continue
        
        if line.startswith("Values:"):
            data_start = True
            i += 1
            continue
        
        if data_start and line:
            parts = line.split()
            try:
                val = int(parts[0])
                if current_row:
                    raw_rows.append(current_row)
                    current_row = []
                for p in parts[1:]:
                    current_row.append(float(p))
            except ValueError:
                for p in parts:
                    try:
                        current_row.append(float(p))
                    except ValueError:
                        pass
        i += 1
    
    if current_row:
        raw_rows.append(current_row)

    return vars_list, np.array(raw_rows)

# --- Main Execution ---
try:
    print(f"Reading raw file from: {raw_file_path}")
    variables, data = parse_ngspice_raw(raw_file_path)
    print(f"Successfully loaded variables: {variables}")

    time = data[:, 0]
    var_dict = {name: idx for idx, name in enumerate(variables)}
    
    t = time
    bl = data[:, var_dict.get('v(bl)', 1)]
    blb = data[:, var_dict.get('v(blb)', 2)]
    out_p = data[:, var_dict.get('v(out_p)', 3)]
    out_n = data[:, var_dict.get('v(out_n)', 4)]
    wl = data[:, var_dict.get('v(wl)', 5)]
    saen = data[:, var_dict.get('v(saen)', 6)]

    # Plotting using Matplotlib
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Subplot 1: Bitlines & Wordline
    ax1.plot(t * 1e9, bl, label='BL (Bitline)', color='blue', linewidth=1.5)
    ax1.plot(t * 1e9, blb, label='BLB (Bitline Bar)', color='red', linewidth=1.5, linestyle='--')
    ax1.plot(t * 1e9, wl * 0.9, label='WL (Wordline x0.9)', color='black', linewidth=1, alpha=0.7)
    ax1.set_ylabel('Voltage (V)')
    ax1.set_title('SRAM Read Path - Bitline Differential Swing & Wordline')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right')

    # Subplot 2: Sense Amplifier Output & Sense Enable
    ax2.plot(t * 1e9, out_p, label='OUT_P', color='green', linewidth=1.5)
    ax2.plot(t * 1e9, out_n, label='OUT_N', color='purple', linewidth=1.5, linestyle='--')
    ax2.plot(t * 1e9, saen * 0.9, label='SAEN (Sense Enable x0.9)', color='orange', linewidth=1, alpha=0.7)
    ax2.set_xlabel('Time (ns)')
    ax2.set_ylabel('Voltage (V)')
    ax2.set_title('Voltage-Latched Sense Amplifier Outputs')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right')

    plt.tight_layout()
    
    # Save plot to results folder
    plt.savefig(output_plot_path, dpi=300)
    print(f"Plot successfully saved to: {output_plot_path}")

    plt.show()

except Exception as i_err:
    print(f"Error parsing or plotting raw file: {i_err}")