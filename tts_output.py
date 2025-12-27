import subprocess
import os
import tempfile
import numpy as np
import scipy.io.wavfile as wav

# Piper dizini ve model dosyası yolları
PIPER_DIR = os.path.join("tts_engine", "piper")
MODEL_PATH = os.path.join(PIPER_DIR, "models", "tr_TR-fahrettin-medium.onnx")
CONFIG_PATH = os.path.join(PIPER_DIR, "models", "tr_TR-fahrettin-medium.onnx.json")
PIPER_EXE = os.path.join(PIPER_DIR, "piper", "piper")

def add_silence_to_start(wav_path, silence_duration_ms=200):
    """WAV dosyasının başına sessizlik ekle"""
    try:
        # WAV dosyasını oku
        sample_rate, audio_data = wav.read(wav_path)

        # Sessizlik süresi (ms -> sample sayısı)
        silence_samples = int(sample_rate * silence_duration_ms / 1000)

        # Sessizlik dizisi oluştur (sıfırlardan oluşan)
        silence = np.zeros(silence_samples, dtype=audio_data.dtype)

        # Sessizlik + orijinal ses
        new_audio = np.concatenate([silence, audio_data])

        # WAV dosyasını yeniden yaz
        wav.write(wav_path, sample_rate, new_audio)
    except Exception as e:
        print(f"⚠️ Sessizlik ekleme hatası (devam ediliyor): {e}")

def synthesize(text, play_audio=True):
    # Geçici WAV dosyası
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav_path = temp_wav.name
    temp_wav.close()

    # İlk kelime atlaması önlemek için başa uzun pause ekle
    text = "... ... " + text

    print(f"🗣️ Konuşma hazırlanıyor: \"{text}\"")

    # Piper komutu (text STDIN'den veriliyor!)
    command = [
        PIPER_EXE,
        "--model", MODEL_PATH,
        "--config", CONFIG_PATH,
        "--output_file", wav_path,
    ]

    try:
        # Metni stdin üzerinden geçir
        subprocess.run(command, input=text.encode("utf-8"), check=True)

        # WAV dosyasına başta sessizlik ekle (ilk kelime atlamasını önle)
        add_silence_to_start(wav_path, silence_duration_ms=200)

        print(f"✅ Ses üretildi: {wav_path}")

        if play_audio:
            if os.name == 'nt':
                os.system(f'start {wav_path}')
            elif os.uname().sysname == 'Darwin':
                os.system(f'afplay {wav_path}')
            else:
                os.system(f'aplay {wav_path}')
        return wav_path

    except subprocess.CalledProcessError as e:
        print("❌ Piper çalışırken hata oluştu:", e)
        return None

# Test
if __name__ == "__main__":
    synthesize("Merhaba efendim, ne yapmamı istersiniz?")
