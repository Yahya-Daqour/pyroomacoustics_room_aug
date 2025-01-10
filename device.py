import librosa
import soundfile as sf
import numpy as np
import pyroomacoustics as pra

# Load audio
input_audio = "data/arctic_a0010-1.wav"
audio, sr = librosa.load(input_audio, sr=None)

# Generate Room Impulse Response (RIR)
room_dim = [5, 5, 3]  # Example room dimensions in meters
mic = [2.5, 2.5, 1.5]  # Mic position
source = [2.8, 2.5, 1.5]  # Source position (30 cm away)
room = pra.ShoeBox(room_dim, fs=sr, absorption=0.2, max_order=10)
room.add_source(source)
room.add_microphone_array(pra.MicrophoneArray(np.array([mic]).T, room.fs))
room.compute_rir()
rir = room.rir[0][0]

# Convolve audio with RIR
convolved_audio = np.convolve(audio, rir)

# Add noise
noise = np.random.normal(0, 0.005, len(convolved_audio))  # Adjust noise level
noisy_audio = convolved_audio + noise

# Save the processed audio
sf.write("output_audio.wav", noisy_audio, sr)
