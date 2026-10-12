# CMOS Sense Amplifier for an SRAM Read Path

Transistor-level design and characterization of a latch-type (cross-coupled) CMOS sense amplifier for an SRAM read path, built entirely with open-source EDA tools on the SkyWater Sky130 process.

**Status:** Baseline 6T SRAM transient testbench is working. Sense amplifier design, characterization, and layout are in progress (see [Roadmap](#roadmap)).

## Tech Stack

| Purpose | Tool |
|---|---|
| Circuit simulation | ngspice (`ngspice_con`) |
| Process models | SkyWater Sky130, 1.8 V devices (`sky130_fd_pr__nfet_01v8`, `sky130_fd_pr__pfet_01v8`) |
| Automation | Python (numpy) for measurement, parsing, and data logging |
| Layout and DRC | KLayout |

## Repository Structure

```text
sramsa/
├── models/     # Sky130 model libraries (sky130_fd_pr/)
├── netlists/   # SPICE subcircuits (sram_cell.spice) and testbenches (sram_tb.spice)
├── results/    # Simulation output (sram_data.txt) and plots
├── scripts/    # Python automation and measurement scripts
├── layout/     # Physical layout files (future phase)
└── notes/      # Design calculations and technical notes
```

## Getting Started

### 1. Install the Sky130 models

```bash
cd models
git clone https://github.com/google/skywater-pdk-libs-sky130_fd_pr.git sky130_fd_pr
```

Testbenches link the models using a relative path:

```spice
.include "../models/sky130_fd_pr/models/sky130.lib.spice"
```

### 2. Run a simulation

```bash
cd netlists
ngspice_con sram_tb.spice
```

Results are written to `results/sram_data.txt` by the `.control` block in the testbench.

## Roadmap

- [x] **Setup and baseline:** repo structure, ngspice and Sky130 integration, inverter characteristics, baseline 6T SRAM transient testbench with automated data output
- [ ] **Read-path fundamentals:** precharge network, bitline swing, cell read current
- [ ] **Sense amplifier design:** topology exploration and device sizing
- [ ] **Timing characterization:** sensing delay and sense-enable timing window
- [ ] **Robustness analysis:** input offset voltage, Monte Carlo variation, process corners
- [ ] **Physical layout:** layout, DRC, and parasitic-aware re-simulation

## License

To be decided.
