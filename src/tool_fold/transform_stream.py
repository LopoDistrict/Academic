import flet as ft
import sounddevice as sd
import soundfile as sf
import numpy as np

def transform_stream(router):
    def start_recording(e):
        nonlocal recording, audio_data
        if not recording:
            recording = True
            recording_state.value = "Recording..."
            start_button.disabled = True
            stop_button.disabled = False
            audio_data = np.zeros((int(seconds * samplerate), 1))  # Prepare array to store audio

            # Ensure we are using the correct input device
            sd.default.device = default_input_device

            # Start recording
            audio_data[:] = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=1, dtype='float32')
            recording_state.update()
            start_button.update()
            stop_button.update()

    def stop_recording(e):
        nonlocal recording, audio_data
        if recording:
            recording = False
            recording_state.value = "Recording stopped."
            start_button.disabled = False
            stop_button.disabled = True
            sd.stop()

            # Save recorded audio
            sf.write('output.wav', audio_data, samplerate)
            recording_state.update()
            start_button.update()
            stop_button.update()

    # Audio settings
    samplerate = 44100  # Sample rate (44.1 kHz)
    seconds = 5  # Duration of recording
    recording = False  # Recording state
    audio_data = np.array([])  # Array to store recorded audio data

    # Detect and set the default input device
    default_input_device = 1
    print(f"Using default input device: {default_input_device}")

    # Flet UI components
    recording_state = ft.Text("Press Start to begin recording.")
    start_button = ft.ElevatedButton("Start", on_click=start_recording)
    stop_button = ft.ElevatedButton("Stop", on_click=stop_recording, disabled=True)

    # Add UI components to the router
    router.add(ft.Column([recording_state, start_button, stop_button]))

if __name__ == "__main__":
    ft.app(target=transform_stream)
