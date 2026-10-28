# 6T SRAM Cell & Voltage-Latched Sense Amplifier Simulation

A robust, load-resilient hybrid SRAM memory architecture featuring a standard 6T SRAM cell subcircuit (`sram_cell.spice`) paired with a CMOS voltage-latched sense amplifier read path. This project implements transistor-level schematic modeling, SPICE transient/DC analyses, and Python-driven waveform automation.

---

## 📊 Simulation Results & Waveforms

> **Note:** The following plots are automatically generated via Python scripts parsing ngspice raw output data to evaluate read stability, sensing delay, and dynamic power dissipation.

### 1. Read/Write Transient Response
![Read and Write Transient Response](assets/transient_response.png)
*Figure 1: Transient voltage waveforms showing successful write operations and stable read cycles without bitline flipping, driven via the `sram_cell.spice` subcircuit netlist.*

### 2. Voltage-Latched Sense Amplifier Differential Output
![Sense Amplifier Waveforms](assets/sense_amp_waveform.png)
*Figure 2: Differential voltage evolution across the cross-coupled inverter nodes of the CMOS voltage-latched sense amplifier during the evaluation phase, highlighting rapid bitline swing resolution.*

### 3. Butterfly Curves & Static Noise Margin (SNM)
![Static Noise Margin Butterfly Curve](assets/snm_butterfly.png)
*Figure 3: VTC-based butterfly curves extracted via DC sweep analysis in ngspice, quantifying the Static Noise Margin (SNM) under hold and read operating conditions.*

---

## 🛠️ Repository Structure

```text
├── spice/
│   ├── sram_cell.spice         # Reusable 6T SRAM cell subcircuit netlist
│   ├── sense_amp.spice         # CMOS voltage-latched sense amplifier schematic
│   └── sram_top_tb.spice       # Top-level testbench for transient and DC analysis
├── scripts/
│   ├── run_simulations.py      # Automation script for executing ngspice batch runs
│   └── plot_waveforms.py       # Python script using Matplotlib/SciPy to generate plots
├── assets/
│   ├── transient_response.png  # Generated transient waveform plot
│   ├── sense_amp_waveform.png  # Generated sense amplifier resolution plot
│   └── snm_butterfly.png       # Extracted SNM butterfly curve plot
└── README.md