import numpy as np
import sounddevice as sd 

sample_rate = 44100 
duration = 5 
frequency = 440 

def generate_sound(frequency, sample_rate, duration): 
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False) 
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t) # 50% volume 
    return sine_wave

def play_sound(): 
    """Generate and play sound in real time.""" 
    print(f"Playing a {frequency} Hz sine wave for {duration} seconds...") 
    sine_wave = generate_sound(frequency, sample_rate, duration) 
    sd.play(sine_wave, samplerate=sample_rate) 
    sd.wait() 

if __name__ == "__main__": 
    play_sound()