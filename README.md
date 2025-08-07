# H.A.Y.D.A.R.

**H.A.Y.D.A.R.** stands for **"Hayatın Akışına Yön Veren Dinamik Akıllı Rehber"**, a Turkish phrase meaning _"A Dynamic Smart Guide That Directs the Flow of Life."_  
Inspired by Iron Man’s **J.A.R.V.I.S.**, this project aims to create a **fully local, character-rich voice assistant** that lives on your personal machine.

---

## 🎯 Goals

- Voice-based interaction (speech-to-text + text-to-speech)
- Local LLM (starting with GPT-OSS-20B or OpenAI API fallback)
- Streamlit (or similar) UI for easy control and testing
- Persona system for humor, character, memory
- Offline-first architecture
- Command handling (print this, search that, turn on lights etc.)
- Modular and extensible codebase
- 3D-printed dummy bot control (long-term goal)

---

## 🛠️ Tech Stack

- Python 3.10+
- Whisper / Whisper.cpp for STT
- Coqui TTS or Piper for TTS
- Streamlit UI (temporary frontend)
- GPT-based brain (OpenAI or open-weight LLM)
- Optional: MQTT / HomeAssistant / CUPS / Linux CLI integration

---

## 🚧 Project Status

> This project is under active development. First step: setting up voice input/output and basic conversation loop.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE.md](./LICENSE.md) file for details.


# H.A.Y.D.A.R. V1 — Voice-to-GPT Personal Assistant

**H.A.Y.D.A.R.** (short for "Highly Adaptive Yet Dependable AI Reactor")  
Version 1 delivers a basic voice-to-AI interaction pipeline using open-source LLMs and speech-to-text tools.

---

## 🧠 What it can do (V1 Features)

- 🎙️ Records your voice via microphone
- 📝 Transcribes speech to Turkish text (using Whisper)
- 🤖 Sends the text to a locally running GPT model (via Ollama)
- 💬 Displays the response on screen
- ⏱️ Measures and logs total GPT response time

---

## 📂 How to Run (Quick Start)

> Requirements:
- Python 3.10+
- [ollama](https://ollama.com/) installed and model gpt-oss:20b downloaded
- ffmpeg, whisper, sounddevice, scipy installed

bash
pip install openai-whisper sounddevice scipy
ollama run gpt-oss:20b
python audio_input.py



## 🛠️ Technologies Used

- OpenAI Whisper for speech-to-text

- Ollama to run LLMs locally

- sounddevice for audio recording

- scipy for WAV file output

### 🔜 What’s Next (Planned for V2)

    - 🗣️ TTS (Text-to-Speech) with a realistic Turkish male voice (e.g., JARVIS-like)

    - 🎭 Personality layer (custom responses like "Efendim?" and tone)

    - 🧱 Modular refactor and first UI shell
