import flet as ft
from . import file_manager
import speech_recognition as sr
import asyncio



class Transcribing():
    def __init__(self):
        self._transcribe_txt = ""
        self.path = "l.wav"
        self.is_paused = False
        self.is_recording = False
        

    async def handle_start_recording(self, e):
        print("start rec")
        await audio_rec.start_recording_async(self.path)

    async def handle_stop_recording(self, e):
        print("stop rec")
        output_path = await audio_rec.stop_recording_async()
        if page.web and output_path is not None:
            await page.launch_url_async(output_path)


    async def handle_pause(self, e):
        print(f"isRecording: {await audio_rec.is_recording_async()}")
        if await audio_rec.is_recording_async():
            await audio_rec.pause_recording_async()

    async def handle_resume(self, e):
        print(f"isPaused: {await audio_rec.is_paused_async()}")
        if await audio_rec.is_paused_async():
            await audio_rec.resume_recording_async()

    def handle_pausing(self, e):
        if not self.is_paused:
            self.handle_resume(e)
        else:
            self.handle_pause(e)
        self.is_paused = not self.is_paused


    def handle_recording(self, e):
        if not self.is_recording:
            self.handle_start_recording(e)
        else:
            self.handle_stop_recording(e)
        self.is_recording = not self.is_recording

    def transcribe_txt_audio(self, audio_path):
        r = sr.Recognizer()                                                       
        audio = sr.AudioFile(audio_path)
        with audio as source:
            audio = r.record(source)
            result = r.recognize_google(audio)
            
        self._transcribe_txt = result


class AI_handling():
    def __init__(self):
        from huggingface_hub import InferenceClient
        self._ai_model = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        self.client = InferenceClient(api_key="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")
        

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
        pass


async def transform_stream(router):
    object_tr = Transcribing()
    object_ai = AI_handling()
    await page.update_async()

    dlg_help = ft.AlertDialog(
        modal=True,
        title=ft.Text("que fait le résumeur de cours"),
        content=ft.Text("""
        Cet outil vous permet d'enregistrer vos cours (CM, TD, TP...) et ensuite en avoir un
        résumé concis. Ce résumé vous pourrez le consultez et l'éditez (il faudra vous rendre
        dans Librairie > [chercher votre fichier] > Ouvrir)
        """),
        actions=[ft.TextButton("Fermer", on_click=lambda e: e.page.close(dlg_help))],
    )

    play_button = ft.IconButton(
        icon=ft.Icons.PLAY_ARROW,
        icon_color="#FFFFFF",
        icon_size=40,
        tooltip="Jouer",
        on_click= lambda e: object_tr.handle_start_recording(e)
    )

    enreg_button = ft.IconButton(
        icon=ft.Icons.STOP_ROUNDED,
        icon_color="#e60f0f",
        icon_size=40,
        tooltip="Delete record",
        on_click=lambda e: object_tr.handle_stop_recording(e)
    )

    time_text = ft.Text("0:15", weight=ft.FontWeight.BOLD)

    temp_listenning = ft.Text("Is listenning")

    page.overlay.append(audio_rec)
    

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.OutlinedButton(
                            text="aide",
                            icon=ft.icons.HELP,
                            on_click=lambda e: e.page.open(dlg_help),
                            adaptive=True,
                            width=100,
                            height=50,
                            icon_color="#0080ff",
                            style=ft.ButtonStyle(color="#0080ff", shape=ft.RoundedRectangleBorder(radius=10)),
                        ),
                    ],

                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(
                    content=ft.Row(
                        [temp_listenning],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            play_button,
                            enreg_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
                ft.Container(
                    ft.Row(                    
                        [time_text],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
    )