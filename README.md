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
  -  `pyroomacoustics`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Yahya-Daqour/pyroomacoustics_room_aug.git
   cd pyroomacoustics_room_aug

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

### Command-Line Arguments
| Argument      | Description                                                    | Default             |
|---------------|----------------------------------------------------------------|---------------------|
| --input_file  | Path to a text file containing WAV files paths (one per line). | Required            |
| --output_dir  | Directory which simulated audios files will be saved.          | Required            |
| --rooms_shape | Room shape: polygon, rectangle, or all                         | all                 |
| --num_rooms   | Number of rooms to generate for simulation                     | 100                 |
| --num_workers | Number of worker processes for parallel processing             | Number of cpu cores |
