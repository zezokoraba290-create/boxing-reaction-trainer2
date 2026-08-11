from random import choice, uniform
from time import time

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform


if platform == "android":
    from plyer import tts

    def speak(text):
        tts.speak(text)

else:
    try:
        import pyttsx3

        engine = pyttsx3.init()

        def speak(text):
            engine.say(text)
            engine.runAndWait()

    except Exception:
        def speak(text):
            print(text)


MOVES = [
    "Jab",
    "Cross",
    "Lead hook",
    "Rear hook",
    "Lead uppercut",
    "Rear uppercut",
    "Slip right",
    "Slip left",
    "Roll right",
    "Roll left",
    "Pull back",
    "Step back",
    "Step left",
    "Step right",
    "Pivot left",
    "Pivot right",
    "Parry",
    "High guard",
]

DURATIONS = [10, 30, 60, 120]


class ReactionTrainer(App):

    def build(self):
        self.running = False
        self.end_time = 0
        self.duration = 30
        self.next_event = None
        self.session_event = None

        root = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15,
        )

        self.title_label = Label(
            text="BOXING REACTION TRAINER",
            font_size="24sp",
            size_hint_y=None,
            height=60,
        )
        root.add_widget(self.title_label)

        self.status = Label(
            text="Choose a duration, then press START",
            font_size="18sp",
        )
        root.add_widget(self.status)

        duration_row = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint_y=None,
            height=55,
        )

        for seconds in DURATIONS:
            button = Button(text=f"{seconds}s")
            button.bind(
                on_press=lambda _, s=seconds: self.set_duration(s)
            )
            duration_row.add_widget(button)

        root.add_widget(duration_row)

        self.start_button = Button(
            text="START",
            font_size="24sp",
            size_hint_y=None,
            height=75,
        )
        self.start_button.bind(on_press=self.start_session)
        root.add_widget(self.start_button)

        self.stop_button = Button(
            text="STOP",
            font_size="24sp",
            size_hint_y=None,
            height=75,
            disabled=True,
        )
        self.stop_button.bind(on_press=self.stop_session)
        root.add_widget(self.stop_button)

        note = Label(
            text="Shadowboxing / footwork only. Keep the movements controlled.",
            font_size="14sp",
            size_hint_y=None,
            height=50,
        )
        root.add_widget(note)

        return root

    def set_duration(self, seconds):
        if not self.running:
            self.duration = seconds
            self.status.text = f"Duration: {seconds} seconds"

    def schedule_next(self, low=0.7, high=2.2):
        if not self.running:
            return

        delay = uniform(low, high)

        self.next_event = Clock.schedule_once(
            self.give_cue,
            delay,
        )

    def give_cue(self, *_):
        if not self.running:
            return

        if time() >= self.end_time:
            self.stop_session()
            return

        move = choice(MOVES)
        self.status.text = move.upper()

        speak(move)

        self.schedule_next()

    def check_session(self, *_):
        if self.running and time() >= self.end_time:
            self.stop_session()

    def start_session(self, *_):
        if self.running:
            return

        self.running = True
        self.end_time = time() + self.duration

        self.start_button.disabled = True
        self.stop_button.disabled = False

        self.status.text = "GET READY..."

        Clock.schedule_once(
            self.give_cue,
            1.2,
        )

        self.session_event = Clock.schedule_interval(
            self.check_session,
            0.1,
        )

    def stop_session(self, *_):
        self.running = False

        if self.next_event is not None:
            self.next_event.cancel()
            self.next_event = None

        if self.session_event is not None:
            self.session_event.cancel()
            self.session_event = None

        self.start_button.disabled = False
        self.stop_button.disabled = True

        self.status.text = "SESSION FINISHED"


if __name__ == "__main__":
    ReactionTrainer().run()