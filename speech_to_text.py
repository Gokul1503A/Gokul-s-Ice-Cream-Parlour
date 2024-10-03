from faster_whisper import WhisperModel

model_size = "small"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

def transcribe(): 

    segments, info = model.transcribe("audio.mp3", beam_size=5)
    text = ""
    for segment in segments:
        text += segment.text
    
    return text

