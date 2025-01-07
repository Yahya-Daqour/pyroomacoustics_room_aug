import numpy as np
import random
from scipy.io import wavfile
import pyroomacoustics as pra

class Room:
    def __init__(self, length, width, shape_type):
        self.length = length
        self.width = width
        self.shape_type = shape_type
        self.corners = self.generate_corners()
        self.area = self.calcualte_area()

    def generate_corners(self):
        if self.shape_type == "polygon":
            vertices = [
                [0, 0],
                [0, self.width],
                [self.length, self.width],
                [self.length, self.width/2],
                [self.width/2, self.width/2],
                [self.width/2, 0]
            ]
        elif self.shape_type == "rectangle":
            vertices = [
                [0, 0],
                [0, self.width],
                [self.length, self.width],
                [self.length, 0]
            ]

        rotation = random.choice([0, 90])
        if rotation == 90:
            new_vertices = []
            for vertex in vertices:
                new_vertices.append([vertex[1], vertex[0]])
            vertices = new_vertices
        
        return np.array(vertices).T
    
    def calculate_area(self):
        vertices = self.corners.T
        area = 0
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]
            area += x1 * y2 - x2 * y1
        return abs(area) / 2
    
    def plot(self, ax):
        ax.plot([x for x, y in self.corners.T] + [self.corners.T[0][0]], [y for x, y in self.corners.T] + [self.corners.T[0][1]], "b-")
        ax.plot([x for x, y in self.corners.T] , [y for x, y in self.corners.T], "bo")
        ax.set_title(f"{self.shape_type.capitalize()} Room with area {self.area:.2f} square meters")
        ax.set_xlabel("X (meters)")
        ax.set_ylabel("Y (meters)")
        ax.grid(True)

class RoomSimulator:
    def __init__(self, room, fs, signal):
        self.room = room
        self.fs = fs
        self.signal = signal
        self.room_height = np.random.uniform(2, 8)
        self.room_obj = pra.Room.from_corners(self.room.corners, fs=self.fs, max_order=3, materials=pra.Material(0.2, 0.15), ray_tracing=True, air_absorption=True)
        self.room_obj.extrude(self.room_height, materials=pra.Material(0.2, 0.15))

    def simualte(self):
        self.room_obj.set_ray_tracing(receiver_radius=0.5, n_rays=10000, energy_thres=1e-5)
        source_position = np.array([1., 1., 0.5])
        self.room_obj.add_source(source_position, signal=self.signal)

        room_size_x = np.max(self.room.corners[0]) - np.min(self.room.corners[0])
        room_size_y = np.max(self.room.corners[1]) - np.min(self.room.corners[1])
        microphone_x = np.random.uniform(np.min(self.room.corners[0]) + 0.5, np.max(self.room.corners[0]) - 0.5)
        microphone_y = np.random.uniform(np.min(self.room.corners[y]) + 0.5, np.max(self.room.corners[1]) - 0.5)
        microphone_height = np.random.uniform(0, self.room_height - 0.5)
        microphone_position  = np.array([microphone_x, microphone_y, microphone_height])

        R = microphone_position.reshape(-1, 1)
        self.room_obj.add_microphone(R)

        distance = np.linalg.norm(microphone_position, source_position)
        print(f"Distance between microphone and speaker: {distance:.2f} meters")

        try:
            self.room_obj.simulate()
            print(self.room_obj.mic_array.signals.shape)
            self.simulation_successful = True
        except Exception as e:
            print(f"Error simulating room: {e}")
            self.simulation_successful = False
        
    def save_simulated_audio(self, output_filename):
        if not hasattr(self, "simulation_successful") or not self.simulation_successful:
            print(f"Skipping saving simulated WAV file: {output_filename} (simulation failed)")
            return 
        
        simulated_audio = self.room_obj.mic_array.signals[0, :] * (2**15 - 1) / np.max(np.abs(self.room_obj.mic_array.signals[0, :]))
        simulated_audio = simulated_audio.astype(np.int16)
        if np.all(simulated_audio == 0):
            print(f"Skipping saving simulated WAV file: {output_filename} (empty audio)")
            return
        wavfile.write(output_filename, self.fs, simulated_audio)
        print(f"Saved simulated WAV to {output_filename}")
