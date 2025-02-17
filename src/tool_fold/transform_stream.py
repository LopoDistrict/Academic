import flet as ft
import sounddevice as sd
import soundfile as sf
import numpy as np
from typing import Union
import speech_recognition as sr
from huggingface_hub import InferenceClient

class AudioTransformation:
    def __init__(self):
        from . import file_manager  # Assuming file_manager is in the same directory
        self.fs = file_manager.FileSystem()
        self.audio_path = self.fs.get_file_path("assets/user_data/tmp.wav")
        self.transcribe_txt_value = ""
        self.recognizer = sr.Recognizer()  # Initialize the recognizer

    def transcribe_txt(self):
        import os
        self.audio_path = str(self.fs.get_file_path("assets/user_data/test.wav"))  # Ensure string path
        print(f"Audio file path: {self.audio_path}")
        print(f"Audio file exists: {os.path.exists(self.audio_path)}")

        if not os.path.exists(self.audio_path):
            raise FileNotFoundError(f"Audio file not found at: {self.audio_path}")

        try:
            with open(self.audio_path, "rb") as audio_file:  # Ensure it's opened as file-like object
                with sr.AudioFile(audio_file) as source:
                    audio = self.recognizer.record(source)
                    result = self.recognizer.recognize_google(audio, language="fr-FR")
                    print(f"Transcription: {self.recognizer.recognize_google(audio, language="fr-FR")}")
                    self.transcribe_txt_value = result

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            print(f"Error, exception: {e}")
        except Exception as ex:
            print(f"Error, exception: {ex}")





class AIHandling:
    def __init__(self):
        self._ai_model = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        self.client = InferenceClient(api_key="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")
        self.text_transcribed = ""

    def get_summary(self, message_stream):
        messages = [
            {"role": "user", "content": f"à l'aide de ce cours crée un résumé: {message_stream}"}
        ]

        stream = self.client.chat.completions.create(
            model="deepseek-ai/deepseek-coder-1.3b-instruct",
            messages=messages,
            temperature=0.3,
            max_tokens=8000,
            top_p=0.7,
            stream=True
        )

        for chunk in stream:
            response_chunk = str(chunk.choices[0].delta.content)
            self.text_transcribed += response_chunk
            print(response_chunk, end="")

    def get_flash_card(self, message_stream):
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

            audio_data = np.zeros((samplerate, 1), dtype='float32')
            sd.default.device = default_input_device
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

            stream.stop()
            stream.close()

            fs = file_manager.FileSystem()
            file_path = fs.get_file_path("assets/user_data/tmp.wav")
            sf.write(file_path, audio_data, samplerate)
            recording_state.update()
            start_button.update()
            stop_button.update()

    def handle_transcription_ai_transform(e):
        show_loader(e)
        transcribe_txt_obj = AudioTransformation()
        ai_obj = AIHandling()

        transcribe_txt_obj.transcribe_txt()
        loading_txt.value = "Création de votre fiche..."
        ai_obj.get_summary(transcribe_txt_obj.transcribe_txt_value)

        e.page.open(dlg_modal)
        hide_loader(e)

    def save_fiche(e):
        e.page.close(dlg_modal)
        from . import file_manager
        fs = file_manager.FileSystem()
        fs.write_to_file(f"document/{nom_fic.value}.md", ai_obj.text_transcribed)

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

    samplerate = 48000
    recording = False
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

    default_input_device = sd.default.device[0]
    print(f"Using default input device: {default_input_device}")

    loading_txt = ft.Text("Transcription en cours... (cela peut prendre un moment)", text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)
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
        on_click=start_recording
    )

    stop_button = ft.IconButton(
        icon=ft.Icons.STOP_ROUNDED,
        icon_color="#e60f0f",
        icon_size=40,
        tooltip="Enreg",
        on_click=stop_recording,
        disabled=True
    )

    nom_fic = ft.TextField(label="Nom du fichier")
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmation"),
        content=ft.Text("Quel nom souhaitez vous donnez à cette fiche?"),
        actions=[
            ft.Column(
                [
                    nom_fic,
                    ft.Row(
                        [
                            ft.TextButton("Sauvegarder", on_click=lambda e: save_fiche(e)),
                        ],
                    ),
                ],
                spacing=25,
            ),
        ],
    )

    content = ft.Column(
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