```python
import flet as ft
import random
import time
import threading


# =========================
# Available movements
# =========================

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


# =========================
# Session durations
# =========================

DURATIONS = [10, 30, 60, 120]


# =========================
# Main application
# =========================

class ReactionTrainer:

    def __init__(self, page: ft.Page):

        self.page = page

        # Session state
        self.running = False
        self.end_time = 0
        self.duration = 30
        self.timer = None

        # =========================
        # Page settings
        # =========================

        page.title = "Boxing Reaction Trainer"

        page.theme_mode = ft.ThemeMode.DARK

        page.bgcolor = ft.Colors.BLACK

        page.padding = 20

        page.vertical_alignment = (
            ft.MainAxisAlignment.CENTER
        )

        page.horizontal_alignment = (
            ft.CrossAxisAlignment.CENTER
        )

        # =========================
        # Title
        # =========================

        self.title = ft.Text(
            "🥊 BOXING REACTION TRAINER",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.RED_400,
            text_align=ft.TextAlign.CENTER,
        )

        # =========================
        # Status
        # =========================

        self.status = ft.Text(
            "Choose duration, then press START",
            size=18,
            color=ft.Colors.WHITE70,
            text_align=ft.TextAlign.CENTER,
        )

        # =========================
        # Current movement
        # =========================

        self.move_display = ft.Text(
            "",
            size=48,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.AMBER,
            text_align=ft.TextAlign.CENTER,
            height=100,
        )

        # =========================
        # Duration buttons
        # =========================

        duration_buttons = []

        for seconds in DURATIONS:

            button = ft.ElevatedButton(
                text=f"{seconds}s",
                width=70,
                on_click=lambda e, s=seconds:
                    self.set_duration(s),
            )

            duration_buttons.append(button)

        self.duration_row = ft.Row(
            controls=duration_buttons,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        # =========================
        # START button
        # =========================

        self.start_btn = ft.ElevatedButton(
            text="START",
            icon=ft.Icons.PLAY_ARROW,
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
            width=150,
            height=50,
            on_click=self.start_session,
        )

        # =========================
        # STOP button
        # =========================

        self.stop_btn = ft.ElevatedButton(
            text="STOP",
            icon=ft.Icons.STOP,
            bgcolor=ft.Colors.RED,
            color=ft.Colors.WHITE,
            width=150,
            height=50,
            on_click=self.stop_session,
            disabled=True,
        )

        # =========================
        # Control buttons row
        # =========================

        self.controls_row = ft.Row(
            controls=[
                self.start_btn,
                self.stop_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        # =========================
        # Note
        # =========================

        self.note = ft.Text(
            "Shadowboxing / footwork only. "
            "Keep movements controlled.",
            size=12,
            color=ft.Colors.GREY_500,
            text_align=ft.TextAlign.CENTER,
        )

        # =========================
        # Add everything to page
        # =========================

        page.add(
            self.title,

            ft.Divider(
                color=ft.Colors.RED_400
            ),

            self.status,

            ft.Container(
                height=20
            ),

            self.move_display,

            ft.Container(
                height=20
            ),

            self.duration_row,

            ft.Container(
                height=20
            ),

            self.controls_row,

            ft.Container(
                height=10
            ),

            self.note,
        )

    # =========================
    # Change duration
    # =========================

    def set_duration(self, seconds):

        if self.running:
            return

        self.duration = seconds

        self.status.value = (
            f"Duration: {seconds} seconds"
        )

        self.page.update()

    # =========================
    # Generate next movement
    # =========================

    def give_cue(self):

        if not self.running:
            return

        # Session finished
        if time.time() >= self.end_time:

            self.stop_session()

            return

        # Select random movement
        move = random.choice(MOVES)

        self.move_display.value = move.upper()

        self.page.update()

        # Random delay between movements
        delay = random.uniform(
            0.7,
            2.2
        )

        self.timer = threading.Timer(
            delay,
            self.give_cue
        )

        self.timer.daemon = True

        self.timer.start()

    # =========================
    # Start session
    # =========================

    def start_session(self, e):

        if self.running:
            return

        self.running = True

        self.end_time = (
            time.time() + self.duration
        )

        # Update buttons
        self.start_btn.disabled = True

        self.stop_btn.disabled = False

        # Update display
        self.status.value = "GET READY..."

        self.move_display.value = ""

        self.page.update()

        # Start after 1.2 seconds
        self.timer = threading.Timer(
            1.2,
            self.give_cue
        )

        self.timer.daemon = True

        self.timer.start()

    # =========================
    # Stop session
    # =========================

    def stop_session(self, e=None):

        self.running = False

        # Cancel active timer
        if self.timer is not None:

            self.timer.cancel()

            self.timer = None

        # Reset buttons
        self.start_btn.disabled = False

        self.stop_btn.disabled = True

        # Reset display
        self.status.value = "SESSION FINISHED"

        self.move_display.value = ""

        self.page.update()


# =========================
# Flet entry point
# =========================

def main(page: ft.Page):

    ReactionTrainer(page)


# =========================
# Run application
# =========================

ft.app(target=main)
```
