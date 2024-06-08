#!/usr/bin/env python3
# author: @caiobegotti
# license: MIT

import argparse
import os
import numpy as np
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
        logging.info(f"Extracted: {audio_path}")
    else:
        logging.info(f"Re-using: {audio_path}")

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

    # normalize energy and arrange it over time
    energy = energy / np.max(energy)
    times = np.arange(len(energy)) * (hop_length / sample_rate)

    # detect peaks in energy that correspond to barks
    peaks, _ = find_peaks(energy, height=0.1, distance=int(0.3 * sample_rate / hop_length))
    bark_count = len(peaks)

    # plot the energy and detected peaks for visualization
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    plot_path = f"{base_name}.png"

    plt.figure(figsize=(14, 6))
    plt.plot(times, energy, label='Noise deviation')
    plt.plot(times[peaks], energy[peaks], 'rx', label='Presumed barks')
    plt.xlabel('Time (mm:ss)')
    plt.ylabel('Normalized energy')
    plt.tight_layout()

    # format x-axis to show time in mm:ss
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x//60):02d}:{int(x%60):02d}"))

    legend = plt.legend(title=f'Maybe {bark_count} barks\n')
    legend.get_frame().set_edgecolor('none')
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()

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
            logging.info(f"Plot: {plot_path}")
            logging.info(f"Barks? Maybe {bark_count}\n")
        except Exception as e:
            logging.error(f"Error processing {video_path}: {e}")

if __name__ == "__main__":
    main()