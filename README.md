# CMOS Sense Amplifier for an SRAM Read Path

A transistor-level design of a latch-type (cross-coupled) CMOS sense amplifier for an SRAM read path, simulated with open-source tools on the SkyWater sky130 process.

**Author:** Anuj Bajpayee
**Status:** Environment setup (Phase 1). No design results yet.

---

## Goal

Design, simulate and characterize a sense amplifier that resolves a small bitline differential into a full-swing digital output, then take the design to layout. The portfolio write-up will cover sizing, sensing delay, input offset and Monte Carlo variation.

## Tool stack

| Purpose | Tool |
|---|---|
| Circuit simulation | ngspice |
| Process models | SkyWater sky130 (1.8 V devices, `sky130_fd_pr__nfet_01v8` / `pfet_01v8`) |
| Measurements and plots | Python (numpy, scipy, matplotlib, pandas) |
| Layout viewing, DRC | KLayout |
| Schematic capture (optional, later) | xschem or Qucs-S |
| Editor | VS Code |
| Version control | Git and GitHub Desktop |

## Repository layout

```
netlists/   SPICE netlists and testbenches
models/     sky130 model files (NOT committed, see below)
results/    plots and measurement output
layout/     layout files (later phase)
scripts/    Python measurement and plotting scripts
notes/      design notes
```

## Setup log (what was done)

Environment setup on a Windows 10 machine:

- [x] Created the project folder structure and initialized the Git repository
- [x] Confirmed ngspice launches (version 31 found, an upgrade to a current release is planned for sky130 model compatibility)
- [ ] Add the newer ngspice to PATH and confirm with `ngspice -v`
- [ ] Install Python and the plotting libraries
- [ ] Install KLayout
- [ ] Clone the sky130 models (see below)
- [ ] Run the RC smoke test (`netlists/rc_test.cir`)
- [ ] Run the sky130 inverter smoke test (`netlists/inv_test.cir`)

Decision record: running the open-source flow in Docker (IIC-OSIC-TOOLS) was evaluated first and dropped, because WSL 2 would not start on this machine. The project uses native Windows tools instead. Layout with Magic and LVS with Netgen are deferred to a later phase on a Linux environment.

## Getting the sky130 models

The models are not stored in this repository. Clone them into `models/`:

```
cd models
git clone https://github.com/google/skywater-pdk-libs-sky130_fd_pr.git sky130_fd_pr
```

Netlists reference them like this (forward slashes, typical corner `tt`):

```
.lib "C:/sramsa/models/sky130_fd_pr/models/sky130.lib.spice" tt
```

## Running a simulation

```
cd netlists
ngspice inv_test.cir
```

## Roadmap

1. Environment setup (this commit)
2. SRAM read-path fundamentals: bitline, precharge, cell read current
3. Latch-type sense amplifier: topology and device sizing
4. Timing: sense enable, sensing delay
5. Input offset and corner analysis
6. Monte Carlo variation
7. Layout, DRC and parasitic-aware re-simulation

## License

To be decided.
