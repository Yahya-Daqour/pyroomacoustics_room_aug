import argparse
import numpy as np
import pandas as pd
import os
from scipy.io import wavfile
import random
from tqdm import tqdm
from utils import Room, RoomSimulator
from concurrent.futures import ProcessPoolExecutor

def simulate_wav_file(wavs_path, rooms, output_dir):
    try:
        # Read the wav file
        fs, signal = wavfile.read(wavs_path)
    except Exception as e:
        print(f"Error reading WAV file: {wavs_path}. Error: {e}")
        return
    
    # Select a random room
    room = random.choice(rooms)

    # Simulate the room
    simulator = RoomSimulator(room, fs, signal)
    simulator.simulate()

    # Save the simulated wav file
    filename = os.path.basename(wavs_path)
    output_filename = os.path.join(output_dir, filename)
    simulator.save_simulated_audio(output_filename)

def main():
    parser = argparse.ArgumentParser(description="Room Simulator")
    parser.add_argument("--input_file", type=str, help="Input file containing WAV file paths")
    parser.add_argument("--output_dir", type=str, help="Output directory for simulated WAV files")
    parser.add_argument("--rooms_shape", type=str, choices=["polygon", "rectangle", "all"], default="all", help="Shape of the rooms (polygon, rectangle, all)")
    parser.add_argument("--num_rooms", type=int, default="100" ,help="Number of rooms to generate")
    parser.add_argument("--num_workers", type=int, default=os.cpu_count() ,help="Number of worker processes")
    args = parser.parse_args()

    # Generate multiple rooms
    rooms = []
    for _ in range(args.num_rooms):
        length = np.random.uniform(3, 10) # 3 to 10 meters
        width = np.random.uniform(2, 6) # 2 to 6 meters
        if args.rooms_shape == "all":
            shape_type = np.random.choice(["polygon", "rectangle"])
        else:
            shape_type = args.rooms_shape
        room = Room(length, width, shape_type)
        rooms.append(room)

    # Store the room details in pandas DataFrame
    data = {
        "Length": [room.length for room in rooms],
        "Width": [room.width for room in rooms],
        "Corners": [room.corners for room in rooms],
        "Area": [room.area for room in rooms],
        "Shape Type": [room.shape_type for room in rooms]
    }
    df = pd.DataFrame(data)
    print("\nMultiple rooms in DataFrame:")
    print(df)

    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Read the input file
    with open(args.input_file, "r", encoding="utf-8") as f:
        wavs_paths = f.readlines()

    # Simulate and save WAV files in parallel
    with ProcessPoolExecutor(max_workers=args.num_workers) as executor:
        futures = []
        for wavs_path in wavs_paths:
            wavs_path = wavs_path.strip()
            futures.append(executor.submit(simulate_wav_file, wavs_path, rooms, args.output_dir))
        for future in tqdm(futures, total=len(wavs_paths)):
            future.result()

if __name__ == "__main__":
    main()