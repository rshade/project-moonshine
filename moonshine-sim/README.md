# Moonshine Simulation Package

This Python package (`moonshine-sim`) provides the core physics engine and design constraints for Project Moonshine.

## Purpose
It allows us to simulate the thermodynamic performance of the **Closed-Loop Organic Rankine Cycle (ORC)** used in our cooling system.

## Setup

Recommended installation (editable mode):

```bash
pip install -e .
```

Or standard installation:

```bash
pip install .
```

## Usage

Run the distiller simulation:

```bash
python moonshine/thermo.py
```

### Sourcing & Impact Analysis
Analyze the environmental and cost trade-offs of different ethanol feedstocks:

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 analyze_sourcing.py
```
