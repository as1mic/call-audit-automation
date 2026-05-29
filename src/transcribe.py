from pathlib import Path

from faster_whisper import WhisperModel

from config import TRANSCRIPTS_DIR

def get_audio_files(folder_path: Path) -> list[Path]:
    if not folder_path.exists():
        return []

    return sorted(
        file_path
        for file_path in folder_path.iterdir()
        if file_path.is_file() and file_path.suffix.lower() == ".mp3"
    )


def parse_audio_filename(filename: str) -> dict[str, str]:
    name = Path(filename).stem
    parts = name.split("_")

    return {
        "date": parts[0] if len(parts) > 0 else "",
        "time": parts[1] if len(parts) > 1 else "",
        "phone": parts[2] if len(parts) > 2 else "",
        "direction": parts[3] if len(parts) > 3 else "",
    }


def transcribe_audio(model, audio_path: Path) -> str:
    segments, info = model.transcribe(
        str(audio_path),
        beam_size=5,
        language="uk",
        vad_filter=True,
    )

    text_pieces = []
    for segment in segments:
        segment_text = segment.text.strip()
        if segment_text:
            text_pieces.append(segment_text)

    full_text = " ".join(text_pieces)

    return full_text.strip()


def save_transcript(audio_path: Path, transcript_text: str) -> Path:
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    transcript_path = TRANSCRIPTS_DIR / (audio_path.stem + ".txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript_text)
    return transcript_path


def get_transcription_model():
    model = WhisperModel("medium", device="cpu", compute_type="int8")

    return model