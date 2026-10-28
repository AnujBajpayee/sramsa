# 6T SRAM Cell & Voltage-Latched Sense Amplifier Simulation

A robust, load-resilient hybrid SRAM memory architecture featuring a standard 6T SRAM cell subcircuit paired with a CMOS voltage-latched sense amplifier read path. This repository contains transistor-level SPICE testbenches, simulation models, and Python automation scripts for waveform analysis and performance evaluation.

---

## Simulation Results & Waveforms

> **Note:** The following plots are automatically generated via Python scripts parsing ngspice output data from simulation runs.

### 1. SRAM Waveform Comparison
![SRAM Waveform Comparison](results/sram%20waveform%20comparision.png)
*Figure 1: Comparative transient waveform analysis showing read/write behavior across test configurations.*

---

## Repository Structure

```text
├── models/
│   ├── sky130_fd_pr/          # SKY130 process design kit models
│   └── ptm130.pm              # Predictive Technology Model (130nm)
├── netlists/
│   ├── sram_cell.spice        # 6T SRAM cell subcircuit netlist
│   ├── sense_amp.spice        # CMOS voltage-latched sense amplifier netlist
│   ├── precharge.spice        # Bitline precharge circuit netlist
│   ├── sram_array_8x4.spice   # 8x4 SRAM array configuration
│   └── tb_*.spice             # Testbenches for cell and array configurations
├── results/
│   ├── raw/                   # Raw ngspice output data files
│   └── sram waveform comparision.png # Generated simulation plots
├── schematics/                # Schematic source files
├── scripts/
│   ├── plot_nosense.py        # Plotting script for non-sense-amp configurations
│   ├── plot_senseamp.py       # Plotting script for sense amplifier path
│   └── plot_sram_comparision.py # Automation script for comparative waveforms
└── README.md