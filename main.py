import flet as ft
import random
import time
import threading


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


class ReactionTrainer:
    def __init__(self, page: ft.Page):
        self.page = page
        self.running = False
        self.end_time = 0
        self.duration = 30
        self.timer = None

        page.title = "Boxing Reaction Trainer"
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = "#000000"
        page.padding = 20
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # العنوان
        self.title = ft.Text(
            "🥊 BOXING REACTION TRAINER",
            size=28,
            weight=ft.FontWeight.BOLD,
            color="#EF5350",
            text_align=ft.TextAlign.CENTER,
        )

        # حالة التطبيق
        self.status = ft.Text(
            "Choose duration, then press START",
            size=18,
            color="#B0B0B0",
            text_align=ft.TextAlign.CENTER,
        )

        # الحركة الحالية
        self.move_display = ft.Text(
            "",
            size=48,
            weight=ft.FontWeight.BOLD,
            color="#FFC107",
            text_align=ft.TextAlign.CENTER,
            height=100,
        )

        # أزرار المدة
        duration_buttons = []
        for sec in DURATIONS:
            btn = ft.ElevatedButton(
                content=ft.Text(f"{sec}s"),
                width=70,
                on_click=lambda e, s=sec: self.set_duration(s),
            )
            duration_buttons.append(btn)

        self.duration_row = ft.Row(
            duration_buttons,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        # زرار START
        self.start_btn = ft.ElevatedButton(
            content=ft.Text("START", color="#FFFFFF"),
            icon=ft.Icons.PLAY_ARROW,
            bgcolor="#4CAF50",
            width=150,
            height=50,
            on_click=self.start_session,
        )

        # زرار STOP
        self.stop_btn = ft.ElevatedButton(
            content=ft.Text("STOP", color="#FFFFFF"),
            icon=ft.Icons.STOP,
            bgcolor="#F44336",
            width=150,
            height=50,
            on_click=self.stop_session,
            disabled=True,
        )

        # صف الأزرار
        self.controls_row = ft.Row(
            [self.start_btn, self.stop_btn],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        # ملاحظة
        self.note = ft.Text(
            "Shadowboxing / footwork only. Keep movements controlled.",
            size=12,
            color="#757575",
            text_align=ft.TextAlign.CENTER,
        )

        # ضيف كل حاجة للصفحة
        page.add(
            self.title,
            ft.Divider(color="#EF5350"),
            self.status,
            ft.Container(height=20),
            self.move_display,
            ft.Container(height=20),
            self.duration_row,
            ft.Container(height=20),
            self.controls_row,
            ft.Container(height=10),
            self.note,
        )

    def set_duration(self, seconds):
        if not self.running:
            self.duration = seconds
            self.status.value = f"Duration: {seconds} seconds"
            self.page.update()

    def give_cue(self):
        if not self.running:
            return

        if time.time() >= self.end_time:
            self.stop_session()
            return

        move = random.choice(MOVES)
        self.move_display.value = move.upper()
        self.page.update()

        # الجولة الجاية
        delay = random.uniform(0.7, 2.2)
        self.timer = threading.Timer(delay, self.give_cue)
        self.timer.start()

    def start_session(self, e):
        if self.running:
            return

        self.running = True
        self.end_time = time.time() + self.duration

        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.status.value = "GET READY..."
        self.move_display.value = ""
        self.page.update()

        # ابدأ بعد 1.2 ثانية
        self.timer = threading.Timer(1.2, self.give_cue)
        self.timer.start()

    def stop_session(self, e=None):
        self.running = False

        if self.timer:
            self.timer.cancel()

        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.status.value = "SESSION FINISHED"
        self.move_display.value = ""
        self.page.update()


def main(page: ft.Page):
    ReactionTrainer(page)


ft.app(target=main)
