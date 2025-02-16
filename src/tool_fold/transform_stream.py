import flet as ft
import sounddevice as sd
import soundfile as sf
import numpy as np
from typing import Union

class Audio_transformation():
    def __init__(self):
        from . import file_manager
        self.fs = file_manager.FileSystem()
        self.audio_path = self.fs.get_file_path("assets/user_data/tmp.wav")
        self.transcribe_txt = ""

    def transcribe_txt(self):
        r = sr.Recognizer()                                                       
        audio = sr.AudioFile(self.audio_path)
        with audio as source:
            audio = r.record(source)
            result = r.recognize_google(audio)
        self._transcribe_txt = result


class AI_handling():
    def __init__(self):
        from huggingface_hub import InferenceClient
        self._ai_model = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        self.client = InferenceClient(api_key="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")
        #self.Aud_obj = Audio_transformation() => on utilise l'objet dans le main 


    def get_summary(self, message_stream):
        messages = [
            {"role": "user", "content": f"à l'aide de ce cours crée un résumé: {message_stream}"}
        ]

        stream = client.chat.completions.create(
            #deepseek-ai/DeepSeek-R1-Distill-Qwen-32B
            #meta-llama/Meta-Llama-3-8B-Instruct
            model="deepseek-ai/deepseek-coder-1.3b-instruct",
            messages=messages,
            temperature=0.3,
            max_tokens=8000,
            top_p=0.7,
            stream=True
        )

        for chunk in stream:
            response_chunk = str(chunk.choices[0].delta.content)
            response_text.value += response_chunk
            response_text.update()
            print(response_chunk, end="")

    def get_flash_card(self, message_stream):
        #pas maintenant peut etre plus tard 
        pass


def transform_stream(router_data: Union[str, None] = None):

    def start_recording(e):
        nonlocal recording, audio_data, stream
        if not recording:
            recording = True
            recording_state.value = "Enregistrement..."
            start_button.disabled = True
            stop_button.disabled = False
            stop_button.icon_color = "#c80f0f"
            

            # Prepare array to store audio
            audio_data = np.zeros((samplerate, 1), dtype='float32')

            # Ensure we are using the correct input device
            sd.default.device = default_input_device

            # Start recording in a non-blocking way
            stream = sd.InputStream(samplerate=samplerate, channels=1, dtype='float32', callback=audio_callback)
            stream.start()

            recording_state.update()
            start_button.update()
            stop_button.update()

    def stop_recording(e):
        from . import file_manager
        nonlocal recording, audio_data, stream
        if recording:
            recording = False
            recording_state.value = "Enregistrement terminé."
            start_button.disabled = False
            stop_button.disabled = True
            start_button.icon_color = "#c5c5c5"
            
            stop_button.icon_color = "#c80f0f"

            # Stop recording
            stream.stop()
            stream.close()

            fs = file_manager.FileSystem()
            file_path = fs.get_file_path("assets/user_data/tmp.wav")

            sf.write(file_path, audio_data, samplerate)
            recording_state.update()
            start_button.update()
            stop_button.update()

    def handle_transcription_ai_transform(e):
        transcribe_txt_obj = Audio_transformation()
        ai_obj = AI_handling()

        transcribe_txt_obj.transcribe_txt()
        loading_txt.value = "Création de votre fiche..."
        ai_obj.get_summary(transcribe_txt_obj)
        

    def show_loader(e):
        e.page.open(loading_alert)
        e.page.update()  

    def hide_loader(e):
        e.page.close(loading_alert)
        e.page.update()

    def audio_callback(indata, frames, time, status):
        nonlocal audio_data
        if recording:
            audio_data = np.append(audio_data, indata)

    samplerate = 48000  # Sample rate (48.0 kHz)
    #seconds = 5  # Duration of recording
    recording = False  # Recording state
    audio_data = np.array([], dtype='float32')
    stream = None 

    dlg_help = ft.AlertDialog(
        modal=True,
        content=ft.Text("""
        Cet outil vous permet d'enregistrer vos cours (CM, TD, TP...) et ensuite en avoir un
        résumé concis. Ce résumé vous pourrez le consultez et l'éditez (il faudra vous rendre
        dans Librairie > [chercher votre fichier] > Ouvrir)
        """),
        actions=[ft.TextButton("Fermer", on_click=lambda e: e.page.close(dlg_help))],
    )


    default_input_device = sd.default.device[0]  # Use the default input device
    print(f"Using default input device: {default_input_device}")

    loading_txt = ft.Text("Transcription en cours...", text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
    loading_alert = ft.AlertDialog(
        content=ft.Container(
            padding=ft.padding.all(20),
            content=ft.Column(
                [
                    loading_txt,
                    ft.ProgressRing(width=36, height=36, stroke_width=4),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            height=70,
        ),
        bgcolor="#314049",
    )
    
    recording_state = ft.Text("Appuyer sur le bouton start pour commencez.")
    start_button = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,
            icon_color="#FFFFFF",
            icon_size=40,
            tooltip="Jouer",
            on_click=start_recording)

    stop_button = ft.IconButton(
            icon=ft.Icons.STOP_ROUNDED,
            icon_color="#e60f0f",
            icon_size=40,
            tooltip="Enreg",
            on_click=stop_recording,
            disabled=True)


    content = ft.Column(
        #juste au dessus on placera les vagues 
        #elles seront juste des vertical divider dans une colonne ou Row
        [
        loading_alert,
        ft.OutlinedButton(
            text="aide",
            icon=ft.icons.HELP,
            on_click=lambda e: e.page.open(dlg_help),
            adaptive=True,
            width=100,
            height=50,
            icon_color="#FFFFFF ",
            style=ft.ButtonStyle(color="#FFFFFF", shape=ft.RoundedRectangleBorder(radius=10)),
        ),
        
        recording_state,
        ft.Container(
            ft.Row(
                [
                    start_button,
                    stop_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ),
        ft.Container(
            ft.Row(
                [
                    ft.FilledButton(
                        text="Transcrire",
                        width=200,
                        height=40,
                        on_click=lambda e: handle_transcription_ai_transform(e),
                        style=ft.ButtonStyle(
                            bgcolor="#2be50a",
                            color="#FFFFFF",
                            overlay_color="#27c00b",
                            shape=ft.RoundedRectangleBorder(radius=7),
                        ),
                    )
                ],
            ),
        ),
    ]
    )

    return content

