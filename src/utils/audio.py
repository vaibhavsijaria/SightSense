import pyaudio
import webrtcvad
import wave
import speech_recognition as sr

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_DURATION_MS = 30
PADDING_DURATION_MS = 1500
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)
NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)
START_OFFSET_CHUNKS = 1
MIN_SILENCE_DURATION_CHUNKS = 20

vad = webrtcvad.Vad(3)
pa = pyaudio.PyAudio()

def is_speech(audio_chunk):
    return vad.is_speech(audio_chunk, RATE)

def record(file_name: str):
    stream = pa.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK_SIZE)
    
    silent_chunks = 0
    frames = []
    speech_started = False

    while True:
        try:
            audio_chunk = stream.read(CHUNK_SIZE)
        except IOError as e:
            if e.errno == pyaudio.paInputOverflowed:
                audio_chunk = '\x00' * CHUNK_SIZE
            else:
                raise

        is_speech_chunk = is_speech(audio_chunk)
        if is_speech_chunk:
            silent_chunks = 0
            if not speech_started:
                print("Recoding started")
                speech_started = True
            frames.append(audio_chunk)
        else:
            if speech_started:
                if silent_chunks < MIN_SILENCE_DURATION_CHUNKS:
                    silent_chunks += 1
                    frames.append(audio_chunk)
                else:
                    print("Recording stopped.")
                    break

    stream.stop_stream()
    stream.close()

    audio = b''.join(frames)

    with wave.open(file_name, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pa.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audio)

def to_text(file_name: str):
    r = sr.Recognizer()
    with sr.AudioFile(file_name) as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print('Cannot recognize')
            return None