import numpy as np
import sounddevice as sd
import cv2


class RealTimeMusicPlayerWithBass:
    def __init__(self, sample_rate=44100, chunk_size=1024, volume=0.5, bass_volume=0.3):
        self.sample_rate = sample_rate  # Samples per second
        self.chunk_size = chunk_size  # Number of audio samples per chunk
        self.volume = volume  # Volume level for melody
        self.bass_volume = bass_volume  # Volume level for bass
        self.time = 0  # Keeps track of time for continuous sine wave
        self.frequency = 440  # Default melody frequency
        self.bass_frequency = 100  # Default bass frequency

    def generate_sine_wave(self, frequency, frames):
        """Generate a sine wave for the given frequency and number of frames."""
        t = np.linspace(self.time, self.time + frames / self.sample_rate, frames, endpoint=False)
        self.time += frames / self.sample_rate  # Update the time for the next chunk
        return self.volume * np.sin(2 * np.pi * frequency * t)

    def generate_bass_wave(self, frames):
        """Generate a sine wave for the bass."""
        t = np.linspace(self.time, self.time + frames / self.sample_rate, frames, endpoint=False)
        return self.bass_volume * np.sin(2 * np.pi * self.bass_frequency * t)

    def audio_callback(self, outdata, frames, time, status):
        """Callback function to send audio data to the output stream."""
        if status:
            print(f"Audio status: {status}")
        melody_wave = self.generate_sine_wave(self.frequency, frames)  # Generate melody sine wave
        bass_wave = self.generate_bass_wave(frames)  # Generate bass sine wave
        composite_wave = melody_wave + bass_wave  # Combine melody and bass
        outdata[:] = composite_wave.reshape(-1, 1)  # Output audio data

        # Update the waveform visualization
        self.plot_waveform_with_opencv(composite_wave)

    def plot_waveform_with_opencv(self, wave):
        """Plot the waveform using OpenCV."""
        canvas = np.ones((300, 800, 3), dtype=np.uint8) * 255  # Create a white canvas
        x = np.linspace(0, canvas.shape[1], len(wave)).astype(np.int32)
        y = (canvas.shape[0] / 2 - wave * (canvas.shape[0] / 2)).astype(np.int32)
        for i in range(len(x) - 1):
            cv2.line(canvas, (x[i], y[i]), (x[i + 1], y[i + 1]), (0, 0, 255), 1)
        cv2.imshow("Waveform", canvas)
        if cv2.waitKey(1) == 27:  # Exit on 'Esc' key
            raise KeyboardInterrupt

    def play_music(self, melody_freqs, bass_freqs, durations, duration_per_note=0.5):
        """Play a melody with dynamic bass and real-time visualization."""
        self.time = 0  # Reset time for clean playback

        with sd.OutputStream(callback=self.audio_callback, channels=1, samplerate=self.sample_rate):
            for i in range(len(melody_freqs)):
                self.frequency = melody_freqs[i]  # Set the current melody frequency
                self.bass_frequency = bass_freqs[i]  # Set the current bass frequency
                sd.sleep(int(durations[i] * 1000))  # Wait for the duration of the note

        cv2.destroyAllWindows()  # Close the waveform window


if __name__ == "__main__":
    # Create a repeating and varied melody with rhythmic "rhymes"
    melody_freqs = [
        262, 294, 330, 349, 392, 440, 494, 523, 440, 349, 330, 294, 262, 220, 349, 330, 220
    ]  # Repeating melody with a rhythmic rhyme
    bass_freqs = [
        65, 73, 82, 87, 98, 110, 123, 131, 110, 87, 82, 73, 65, 55, 87, 82, 55
    ]  # Complementary bass frequencies
    durations = [
        0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 1
    ]  # Rhythmic pattern for each note

    # Create an instance of the RealTimeMusicPlayerWithBass class
    music_player = RealTimeMusicPlayerWithBass(sample_rate=44100, chunk_size=1024, volume=0.5, bass_volume=0.3)

    # Play the melody with bass and real-time waveform plotting
    try:
        music_player.play_music(melody_freqs, bass_freqs, durations, duration_per_note=0.5)
    except KeyboardInterrupt:
        print("Playback interrupted.")
