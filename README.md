# Boxing Reaction Trainer

A simple Kivy Android app for controlled shadowboxing/footwork reaction practice.

## Features
- Random boxing/footwork cues.
- Random delay between cues.
- Session durations: 10, 30, 60, 120 seconds.
- Android text-to-speech through Plyer.
- Desktop fallback to pyttsx3.

## Important
The cue list is intended for controlled shadowboxing and footwork practice, not contact drills.

## Android build
Buildozer is normally used through Linux/WSL on Windows.

Inside WSL/Ubuntu, put this project in your Linux home directory, then:

    buildozer init

If buildozer.spec already exists, do not run init again.

Install Buildozer and follow its current Android setup instructions, then:

    buildozer -v android debug

The APK will be created in the `bin/` directory.

For Windows + WSL, build from the WSL filesystem (for example `~/boxing_reaction_trainer`) rather than `/mnt/c/...`.
