import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
import tempfile
import ollama
import time
import signal
from contextlib import contextmanager
from tts_output import synthesize
from haydar_persona import haydar

# Ses parametreleri
DURATION = 5  # saniye
SAMPLERATE = 44100  # 44.1 kHz CD kalitesi
LLM_TIMEOUT = 60  # LLM yanıt timeout süresi (saniye) - CPU için artırıldı

# Whisper modelini global olarak yükle (her seferinde yeniden yüklemeyi önle)
print("🔄 Whisper modeli yükleniyor...")
WHISPER_MODEL = whisper.load_model("medium")
print("✅ Whisper modeli hazır!")

class TimeoutError(Exception):
    pass

@contextmanager
def time_limit(seconds):
    """Timeout context manager"""
    def signal_handler(signum, frame):
        raise TimeoutError("LLM yanıtı zaman aşımına uğradı")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def record_audio(duration=DURATION):
    print("🎙️ Dinliyorum...")

    recording = sd.rec(int(duration * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()

    # Ses seviyesini kontrol et
    max_amplitude = np.abs(recording).max()
    print(f"🔊 Maksimum ses seviyesi: {max_amplitude}")

    if max_amplitude < 100:
        print("⚠️ UYARI: Mikrofon ses algılamıyor! Lütfen mikrofon ayarlarınızı kontrol edin.")

    # Geçici WAV dosyasına kaydet
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_wav.name, SAMPLERATE, recording)

    print(f"✅ Ses kaydedildi: {temp_wav.name}")
    return temp_wav.name

def transcribe_audio(audio_path):
    print("📝 Ses yazıya dönüştürülüyor...")

    try:
        # Ses dosyasını kontrol et
        sample_rate, audio_data = wav.read(audio_path)

        # Ses seviyesini kontrol et (çok sessiz mi?)
        audio_amplitude = np.abs(audio_data).max()
        if audio_amplitude < 100:  # Çok düşük ses seviyesi
            print("⚠️ Ses algılanamadı (çok sessiz)")
            return ""

        # Global model kullan (her seferinde yeniden yükleme yok)
        result = WHISPER_MODEL.transcribe(audio_path, language='tr')

        # Boşlukları temizle
        text = result['text'].strip()

        print(f"📄 Metin: {text}")
        return text

    except Exception as e:
        print(f"❌ Transkripsiyon hatası: {e}")
        return ""

def listen_and_transcribe():
    audio_path = record_audio()
    text = transcribe_audio(audio_path)
    return text

def get_gpt_response(prompt, speak=True):
    print("🧠 H.A.Y.D.A.R. düşünüyor...")
    start_time = time.time()

    # Intent algılama
    intent = haydar.detect_intent(prompt)

    # Eğer hazır yanıt varsa kullan (hızlı)
    canned_response = haydar.get_canned_response(intent)
    if canned_response:
        message = canned_response
        duration = time.time() - start_time
    else:
        # LLM'den yanıt al
        try:
            messages = [{'role': 'system', 'content': haydar.get_system_prompt()}]

            # Konuşma geçmişini ekle (context)
            messages.extend(haydar.get_conversation_context())

            # Yeni soruyu ekle
            messages.append({'role': 'user', 'content': prompt})

            # Timeout ile LLM çağrısı
            with time_limit(LLM_TIMEOUT):
                response = ollama.chat(
                    model='qwen2.5:7b',
                    messages=messages,
                    options={
                        'temperature': 0.7,  # Daha tutarlı (0-2 arası, default 0.8)
                        'top_p': 0.9,
                    }
                )

            duration = time.time() - start_time
            message = response['message']['content']

        except TimeoutError as e:
            duration = time.time() - start_time
            message = f"Üzgünüm efendim, yanıt verirken zaman aşımı oluştu. Lütfen daha kısa bir soru sorun veya tekrar deneyin."
            print(f"⚠️ Timeout: {e}")

        except Exception as e:
            duration = time.time() - start_time
            message = f"Üzgünüm efendim, bir hata oluştu: {str(e)}"
            print(f"❌ Hata: {e}")

    # Conversation history'ye ekle
    haydar.add_to_history(prompt, message)

    print(f"💬 Yanıt: {message}")
    print(f"⏱️ Süre: {duration:.2f} saniye")

    # TTS ile yanıtı seslendir
    if speak:
        print("🔊 H.A.Y.D.A.R. konuşuyor...")
        synthesize(message, play_audio=True)

    return message

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 H.A.Y.D.A.R. AI - Sesli Asistan")
    print("=" * 50)
    print("💡 Çıkmak için: 'çıkış', 'görüşürüz' veya 'kapat'")
    print()

    # Sürekli konuşma döngüsü
    while True:
        print("\n" + "─" * 50)
        print("📌 Mikrofona konuşun (5 saniye)")

        input_text = listen_and_transcribe()
        print(f"🔊 Siz: {input_text}")

        # Boş input kontrolü
        if not input_text or len(input_text.strip()) == 0:
            print("⚠️ Ses algılanamadı, lütfen tekrar deneyin.")
            continue

        # Çıkış komutları kontrolü
        exit_commands = ['çıkış', 'çık', 'görüşürüz', 'kapat', 'bye', 'exit', 'hoşça kal', 'güle güle']
        if any(cmd in input_text.lower() for cmd in exit_commands):
            # Vedalaşma mesajını söyle (goodbye canned response)
            goodbye_msg = haydar.get_canned_response('goodbye')
            print(f"\n💬 {goodbye_msg}")
            synthesize(goodbye_msg, play_audio=True)
            print("\n👋 Programdan çıkılıyor...")
            break

        print()
        get_gpt_response(input_text, speak=True)

