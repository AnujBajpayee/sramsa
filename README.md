# 6T SRAM Read Path & Voltage-Latched Sense Amplifier (VLSA)

A SPICE-based simulation framework for the **read path of a 6T SRAM**: bitcell, bitline pre-charge/equalization, and a **voltage-latched sense amplifier**. It is simulated in **Ngspice** using the **ASU Predictive Technology Model (PTM) 130 nm** (BSIM4, `level=54`), with a **Python** script for automated waveform parsing and plotting.

![Simulation waveforms](results/sram_waveforms.png)

---

## Highlights

- Physics-based BSIM4 transistor models (PTM 130 nm), not idealized switches
- Complete read sequence: **pre-charge → equalize → wordline assertion → bitline differential development → sense-enable → latch resolution**
- Fully scripted flow: simulate with Ngspice, then parse the raw output and plot with Python
- Reproducible, plain-text netlists that are easy to modify and extend

---

## Project Structure

```text
C:\sramsa\
├── models\
│   └── ptm\
│       └── ptm130.pm          # ASU PTM 130nm BSIM4 transistor models
├── netlists\
│   ├── sram_cell.spice        # Subcircuits: 6T cell, pre-charge, sense amplifier
│   └── sram_tb.spice          # Top-level testbench, stimuli and control blocks
├── results\
│   ├── sram_tran.raw          # Ngspice raw transient data (generated)
│   └── sram_waveforms.png     # Plotted waveforms (generated)
├── plot_sram.py               # Raw-file parser and waveform plotter
└── README.md                  # Project documentation
```

---

## Circuit Overview

| Block | Subcircuit | Description |
|-------|-----------|-------------|
| 6T bitcell | `sram_6t` | Two cross-coupled CMOS inverters plus two NMOS access transistors, gated by the wordline (`WL`) and connected to the complementary bitlines (`BL`, `BLB`). |
| Pre-charge & equalizer | `sram_precharge` | Pre-charges both bitlines to the **1.8 V** rail and equalizes them before each access, so the sense amp starts from a balanced state. |
| Voltage-latched sense amp | `voltage_sense_amp` | On assertion of sense-enable (`SAEN`), amplifies the small bitline differential (ΔV_BL) via positive-feedback regeneration into full rail-to-rail outputs (`OUT_P`, `OUT_N`). |

### Read Operation Sequence

1. **Pre-charge / equalize:** `BL` and `BLB` are driven to VDD (1.8 V) and equalized.
2. **Wordline on:** `WL` is asserted and the cell discharges one bitline, developing a differential ΔV_BL.
3. **Sense enable:** once ΔV_BL is sufficient, `SAEN` fires and the latch regenerates.
4. **Resolve:** `OUT_P` / `OUT_N` settle to complementary full-swing digital levels.

---

## Prerequisites

| Tool | Purpose |
|------|---------|
| [Ngspice](https://ngspice.sourceforge.io/) | Circuit simulation (must be on your `PATH`) |
| Python 3.8+ | Waveform parsing and plotting |
| `numpy`, `matplotlib` | Python plotting dependencies |

Install the Python dependencies:

```powershell
pip install numpy matplotlib
```

---

## Running the Simulation

**1. Run the transient simulation**

```powershell
cd C:\sramsa\netlists
ngspice sram_tb.spice
```

This runs the transient analysis and writes the raw data to `C:\sramsa\results\sram_tran.raw`.

**2. Generate waveform plots**

```powershell
python C:\sramsa\plot_sram.py
```

The script displays an interactive plot of `BL`, `BLB`, `WL`, `SAEN`, `OUT_P` and `OUT_N`, and saves a high-resolution copy to `C:\sramsa\results\sram_waveforms.png`.

---

## Customizing the Simulation

- **Supply / timing:** edit the supply and the `WL`/`SAEN`/pre-charge pulse definitions in `netlists/sram_tb.spice`.
- **Transistor sizing:** adjust W/L in `netlists/sram_cell.spice` (cell ratio, sense-amp latch devices).
- **Process models:** swap `models/ptm/ptm130.pm` for another PTM node and update the `.include` path in the testbench.

---

## Possible Extensions

- Monte Carlo mismatch analysis for sense-amp input-referred offset
- Sensing-margin sweep vs. `SAEN` timing and bitline differential
- Temperature and supply corners
- Comparison with a current-latched sense amplifier (CLSA)
- Layout and parasitic extraction (PEX) of the read path

---

##