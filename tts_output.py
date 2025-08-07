import subprocess
import os
import tempfile

# Piper dizini ve model dosyası yolları
PIPER_DIR = os.path.join("tts_engine", "piper")
MODEL_PATH = os.path.join(PIPER_DIR, "models", "tr_TR-fahrettin-medium.onnx")
CONFIG_PATH = os.path.join(PIPER_DIR, "models", "tr_TR-fahrettin-medium.onnx.json")
PIPER_EXE = os.path.join(PIPER_DIR, "piper.exe")

def synthesize(text, play_audio=True):
    # Geçici WAV dosyası
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav_path = temp_wav.name
    temp_wav.close()

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

        print(f"✅ Ses üretildi: {wav_path}")

        if play_audio:
            os.system(f'start {wav_path}' if os.name == 'nt' else f'afplay {wav_path}')
        return wav_path

    except subprocess.CalledProcessError as e:
        print("❌ Piper çalışırken hata oluştu:", e)
        return None

# Test
if __name__ == "__main__":
    synthesize("Merhaba efendim, ne yapmamı istersiniz?")
