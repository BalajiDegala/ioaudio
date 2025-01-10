import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
sample_rate = 44100  # Samples per second
duration = 5  # Duration of the sound in seconds
frequency = 44  # Frequency of the sine wave (A4 note)
volume = 0.5  # Volume level

# Generate the initial sine wave
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
print(t)
sine_wave = volume * np.sin(2 * np.pi * frequency * t)

# Set up the figure for plotting
fig, ax = plt.subplots(figsize=(10, 4))
line, = ax.plot([], [], lw=2)
ax.set_xlim(0, 0.1)  # Show only 0.1 seconds of data for clarity
ax.set_ylim(-1, 1)
ax.set_title(f"Sine Wave: {frequency} Hz")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.grid()

# Initialize variables
current_frame = 0
chunk_size = 1024  # Number of samples per callback

def update_plot(frame):
    """Update the plot for animation."""
    global current_frame
    start = current_frame * chunk_size
    end = start + chunk_size

    # Handle case where we exceed the wave length
    if start >= len(sine_wave):
        return line,

    time_segment = t[start:end]
    sine_segment = sine_wave[start:end]

    line.set_data(time_segment, sine_segment)
    return line,

def audio_callback(outdata, frames, time, status):
    """Callback function for sounddevice to generate audio in real-time."""
    global current_frame
    # if status:
    #     print(status)

    start = current_frame * chunk_size
    end = start + frames

    # Handle underflow (remaining samples less than requested)
    if end > len(sine_wave):
        remaining_samples = len(sine_wave) - start
        outdata[:remaining_samples] = sine_wave[start:].reshape(-1, 1)
        outdata[remaining_samples:] = 0  # Fill the rest with silence
        raise sd.CallbackStop()  # Stop playback after this chunk
    else:
        outdata[:] = sine_wave[start:end].reshape(-1, 1)

    current_frame += 1

# Create the animation object
ani = animation.FuncAnimation(fig, update_plot, frames=range(0, int(sample_rate * duration / chunk_size)), interval=50, blit=True)

# Display the plot and play the sound
def start_audio_and_visualization():
    with sd.OutputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
        plt.show()  # Show the plot and start updating it


start_audio_and_visualization()
