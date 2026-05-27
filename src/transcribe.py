from pathlib import Path


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


def transcribe_audio(audio_path: Path) -> str:
    # TODO: replace with real transcription logic.
    return f"Transcription placeholder for {audio_path.name}"