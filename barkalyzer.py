#!/usr/bin/env python3
# author: @caiobegotti
# license: MIT

import argparse
import os
import numpy as np
import librosa
import logging
import matplotlib.pyplot as plt
import moviepy.editor as mp
import glob

from scipy.io import wavfile
from scipy.signal import find_peaks

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def extract_audio(video_path, force):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = f"{base_name}.wav"

    if not os.path.exists(audio_path) or force:
        video = mp.VideoFileClip(video_path)

        # leave it on the disk to re-use it in the future
        audio = video.audio
        audio.write_audiofile(audio_path, logger=None)
        logging.info(f"Audio extracted: {audio_path}")
    else:
        logging.info(f"Using existing audio file: {audio_path}")

    return audio_path

def analyze_audio(audio_path):
    sample_rate, audio_data = wavfile.read(audio_path)

    # convert to mono if stereo
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)

    # calculate the short-term energy
    frame_length = 2048
    hop_length = 512
    energy = np.array([
        np.sum(np.abs(audio_data[i:i + frame_length] ** 2))
        for i in range(0, len(audio_data), hop_length)
    ])

    # normalize energy
    energy = energy / np.max(energy)

    # detect peaks in energy that correspond to barks
    peaks, _ = find_peaks(energy, height=0.1, distance=int(0.3 * sample_rate / hop_length))

    # plot the energy and detected peaks for visualization
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    plot_path = f"{base_name}.png"

    plt.figure(figsize=(14, 6))
    plt.plot(energy, label='Noise energy')
    plt.plot(peaks, energy[peaks], 'rx', label='Presumed barks')
    plt.xlabel('Frame')
    plt.ylabel('Normalized energy')
    plt.legend()
    plt.savefig(plot_path)
    plt.close()

    bark_count = len(peaks)
    return bark_count, plot_path

def main():
    parser = argparse.ArgumentParser(description="Analyze my security cam streams to detect and plot when my dog barks.")
    parser.add_argument("video_paths", nargs='+', type=str, help="Paths to one or more input video files")
    parser.add_argument("-f", "--force", action="store_true", help="Force re-extraction of audio")

    args = parser.parse_args()
    video_paths = []
    for pattern in args.video_paths:
        video_paths.extend(glob.glob(pattern))

    for video_path in video_paths:
        try:
            audio_path = extract_audio(video_path, args.force)
            bark_count, plot_path = analyze_audio(audio_path)
            logging.info(f"Plot saved: {plot_path}")
            logging.info(f"Barks detected: {bark_count}\n")
        except:
            logging.error(f"Error processing {video_path}: {e}")

if __name__ == "__main__":
    main()