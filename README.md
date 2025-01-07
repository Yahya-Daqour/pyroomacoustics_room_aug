# Pyroomacoustics Room Simulator


This repository contains a Python application for simulating room acoustics and applying the simulated effects to WAV audio files. The simulation is based on user-defined room dimensions, shapes, and acoustic characteristics.

## Features

- Simulates room acoustics for audio files using randomly generated rooms dimensions and shapes.
- Supports polygonal and rectangular room shapes.
- Parallel processing of audio files to optimize runtime.
- Generates room details (length, width, corners, area, shape type) and exports them as a pandas DataFrame.

## Requirements

- Python 3.7 or higher
- Required Python packages (install via `pip`):
  - `numpy`
  - `pandas`
  - `scipy`
  - `tqdm`

## Installation

1. Clone the repository:

   ```bash
   git clone [<repository-url>](https://github.com/Yahya-Daqour/pyroomacoustics_room_aug.git)
   cd pyroomacoustics_room_aug
