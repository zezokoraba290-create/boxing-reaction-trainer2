import flet as ft
import flet_audio as fta
import random
import time
import threading


# اسم كل حركة + اسم ملف الصوت المرتبط بيها (في مجلد assets/sounds)
MOVES = [
    ("Jab", "jab.mp3"),
    ("Cross", "cross.mp3"),
    ("Lead hook", "lead_hook.mp3"),
    ("Rear hook", "rear_hook.mp3"),
    ("Lead uppercut", "lead_uppercut.mp3"),
    ("Rear uppercut", "rear_uppercut.mp3"),
    ("Slip right", "slip_right.mp3"),
    ("Slip left", "slip_left.mp3"),
    ("Roll right", "roll_right.mp3"),
    ("Roll left", "roll_left.mp3"),
    ("Pull back", "pull_back.mp3"),
    ("Step back", "step_back.mp3"),
    ("Step left", "step_left.mp3"),
    ("Step right", "step_right.mp3"),
    ("Pivot left", "pivot_left.mp3"),
    ("Pivot right", "pivot_right.mp3"),
    ("Parry", "parry.mp3"),
    ("High guard", "high_guard.mp3"),
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

        # عنصر الصوت (بيشتغل من غير ما يتشاف على الشاشة)
        self.audio_player = fta.Audio(
            src="",
            autoplay=False,
            volume=1.0,
            on_loaded=lambda e: print("AUDIO: loaded", flush=True),
            on_state_change=lambda e: print(f"AUDIO: state changed -> {e.data}", flush=True),
        )
        page.overlay.append(self.audio_player)

        # وقف أي تايمر شغال لو المستخدم قفل نافذة التطبيق
        page.on_disconnect = lambda e: self.stop_session()

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

        # زرار تجربة الصوت (للتأكد إن الصوت شغال أصلاً)
        self.test_sound_btn = ft.ElevatedButton(
            content=ft.Text("🔊 TEST SOUND"),
            width=150,
            height=40,
            on_click=lambda e: self.play_sound("jab.mp3"),
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
            self.test_sound_btn,
            ft.Container(height=10),
            self.note,
        )

    def set_duration(self, seconds):
        if not self.running:
            self.duration = seconds
            self.status.value = f"Duration: {seconds} seconds"
            self.page.update()

    async def _safe_play(self):
        """يشغل الصوت من الأول"""
        print(f"AUDIO: trying to play -> {self.audio_player.src}", flush=True)
        try:
            await self.audio_player.play()
            print("AUDIO: play() returned successfully", flush=True)
        except Exception as ex:
            print(f"AUDIO: play() error -> {ex}", flush=True)

    def play_sound(self, filename: str):
        """يشغل ملف الصوت المرتبط بالحركة"""
        self.audio_player.src = f"sounds/{filename}"
        self.audio_player.update()
        # play() بقت async في نسخة flet-audio الحديثة، فبنشغلها
        # على event loop الصفحة عشان تشتغل بأمان من جوه الـ Timer thread
        self.page.run_task(self._safe_play)

    def give_cue(self):
        if not self.running:
            return

        if time.time() >= self.end_time:
            self.stop_session()
            return

        move_name, sound_file = random.choice(MOVES)
        self.move_display.value = move_name.upper()
        self.page.update()
        self.play_sound(sound_file)

        # الجولة الجاية - أقل مسافة 1.5 ثانية عشان الكلمة تتقال كاملة قبل الحركة الجاية
        delay = random.uniform(1.5, 3.0)
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
        try:
            self.page.update()
        except Exception:
            # الصفحة ممكن تكون اتقفلت خلاص (زي إقفال نافذة التطبيق)
            pass


def main(page: ft.Page):
    ReactionTrainer(page)


ft.app(target=main, assets_dir="assets")
