import os
import subprocess
from pathlib import Path

# -----------------------------
# 1️⃣ Project folder ke paths
# -----------------------------
PROJECT_ROOT = Path(__file__).parent.parent  # src/ se ek level upar
FFMPEG_PATH = PROJECT_ROOT / "ffmpeg" / "ffmpeg.exe"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Create output folder if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# 2️⃣ FFmpeg check
# -----------------------------
try:
    result = subprocess.run([str(FFMPEG_PATH), "-version"], capture_output=True, text=True)
    print("FFmpeg found!")
    print(result.stdout.splitlines()[0])
except FileNotFoundError:
    print("FFmpeg nahi mila! Check karo 'ffmpeg' folder aur path.")
    exit(1)

# -----------------------------
# 3️⃣ Convert audio/video to WAV
# -----------------------------
def convert_to_wav(input_file, output_file):
    """Convert audio/video to WAV using local FFmpeg."""
    subprocess.run([str(FFMPEG_PATH), "-y", "-i", str(input_file), str(output_file)])
    print(f"Converted {input_file.name} → {output_file.name}")

# -----------------------------
# 4️⃣ Whisper transcription
# -----------------------------
def transcribe_audio(audio_file):
    """Transcribe using Whisper (Python package)."""
    try:
        import whisper
    except ImportError:
        print("Whisper installed nahi hai. Run: pip install openai-whisper")
        exit(1)
    
    model = whisper.load_model("small")  # small/medium/large
    result = model.transcribe(str(audio_file))
    return result["text"]

# -----------------------------
# 5️⃣ Main workflow
# -----------------------------
def main():
    for file in DATA_DIR.iterdir():
        if file.suffix.lower() not in [".mp3", ".wav", ".m4a"]:
            continue

        wav_file = OUTPUT_DIR / (file.stem + ".wav")
        convert_to_wav(file, wav_file)

        print(f"Transcribing {wav_file.name} ...")
        text = transcribe_audio(wav_file)

        output_text_file = OUTPUT_DIR / (file.stem + ".txt")
        output_text_file.write_text(text, encoding="utf-8")
        print(f"Saved transcription: {output_text_file.name}\n")

if __name__ == "__main__":
    main()
