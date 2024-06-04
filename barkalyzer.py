#!/usr/bin/env python3

import argparse
import os
import numpy as np
import librosa
import logging
import matplotlib.pyplot as plt
import moviepy.editor as mp

from scipy.io import wavfile
from scipy.signal import find_peaks

logging.getLogger("moviepy").setLevel(logging.ERROR)

def extract_audio(video_path, force):
    # Extract the file name without extension
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    # Create the output audio file path
    audio_path = f"{base_name}.wav"

    if not os.path.exists(audio_path) or force:
        # Load the video file
        video = mp.VideoFileClip(video_path)

        # Extract audio
        audio = video.audio
        audio.write_audiofile(audio_path, logger=none)
        print(f"Audio extracted to: {audio_path}")
    else:
        print(f"Using existing audio file: {audio_path}")

    return audio_path

def analyze_audio(audio_path):
    # Load the audio file
    sample_rate, audio_data = wavfile.read(audio_path)

    # Convert to mono if stereo
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)

    # Calculate the short-term energy
    frame_length = 2048
    hop_length = 512
    energy = np.array([sum(abs(audio_data[i:i+frame_length]**2)) for i in range(0, len(audio_data), hop_length)])

    # Normalize energy
    energy = energy / np.max(energy)

    # Detect peaks in energy that correspond to barks
    peaks, _ = find_peaks(energy, height=0.3, distance=int(0.5 * sample_rate / hop_length))

    # Extract the file name without extension
    base_name = os.path.splitext(os.path.basename(audio_path))[0]

    # Plot the energy and detected peaks for visualization
    plt.figure(figsize=(14, 6))
    plt.plot(energy, label='Energy')
    plt.plot(peaks, energy[peaks], 'rx', label='Barks')
    plt.title('Bark Detection in Audio')
    plt.xlabel('Frame')
    plt.ylabel('Normalized Energy')
    plt.legend()
    
    # Save the plot as a PNG file
    plot_path = f"{base_name}.png"
    plt.savefig(plot_path)
    plt.close()

    # Count the number of distinct barks
    bark_count = len(peaks)
    return bark_count, plot_path

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Extract audio from video file and analyze it.")
    parser.add_argument("video_path", type=str, help="Path to the input video file")
    parser.add_argument("-f", "--force", action="store_true", help="Force re-extraction of audio")

    # Parse the arguments
    args = parser.parse_args()

    # Extract audio from the video
    audio_path = extract_audio(args.video_path, args.force)

    # Analyze the audio
    bark_count, plot_path = analyze_audio(audio_path)
    print(f"Plot saved to: {plot_path}")
    print(f"Number of barks detected: {bark_count}")

if __name__ == "__main__":
    main()