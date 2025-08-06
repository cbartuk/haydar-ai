import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
import tempfile

# Ses parametreleri
DURATION = 5  # saniye cinsinden kayıt süresi
SAMPLERATE = 44100  # 44.1kHz CD kalitesinde

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
    print("🔍 Ses yazıya dönüştürülüyor...")
    model = whisper.load_model("base")  # veya "small", "medium", "large"
    result = model.transcribe(audio_path, language='tr')  # Türkçe varsayımı
    print(f"📝 Yazı: {result['text']}")
    return result['text']

def listen_and_transcribe():
    audio_file = record_audio()
    text = transcribe_audio(audio_file)
    return text

# Test (isteğe bağlı)
if __name__ == "__main__":
    output = listen_and_transcribe()
    print("🎧 Duyulan:", output)
