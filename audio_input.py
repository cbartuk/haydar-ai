import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
import tempfile
import ollama
import time

# Ses parametreleri
DURATION = 5  # saniye
SAMPLERATE = 44100  # 44.1 kHz CD kalitesi

def record_audio(duration=DURATION):
    print("🎙️ Dinliyorum...")

    recording = sd.rec(int(duration * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()

    # Geçici WAV dosyasına kaydet
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_wav.name, SAMPLERATE, recording)

    print(f"✅ Ses kaydedildi: {temp_wav.name}")
    return temp_wav.name

def transcribe_audio(audio_path):
    print("📝 Ses yazıya dönüştürülüyor...")

    # Cuda destekliyorsa burayı device='cuda' yapabilirsin
    model = whisper.load_model("base")  # veya whisper.load_model("base", device="cuda")
    result = model.transcribe(audio_path, language='tr')

    print(f"📄 Metin: {result['text']}")
    return result['text']

def listen_and_transcribe():
    audio_path = record_audio()
    text = transcribe_audio(audio_path)
    return text

def get_gpt_response(prompt):
    print("🧠 H.A.Y.D.A.R. düşünüyor...")
    start_time = time.time()

    response = ollama.chat(
        model='gpt-oss:20b',
        messages=[{'role': 'user', 'content': prompt}]
    )

    duration = time.time() - start_time
    message = response['message']['content']

    print(f"💬 Yanıt: {message}")
    print(f"⏱️ Süre: {duration:.2f} saniye")
    return message

if __name__ == "__main__":
    input_text = listen_and_transcribe()
    print("🔊 Algılanan:", input_text)

    get_gpt_response(input_text)
