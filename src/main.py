from config import AUDIO_DIR
from transcribe import get_audio_files, parse_audio_filename


def main() -> None:
    audio_files = get_audio_files(AUDIO_DIR)
    print(f"Found {len(audio_files)} audio files in {AUDIO_DIR}")

    for audio_file in audio_files:
        metadata = parse_audio_filename(audio_file.name)
        print(f"- {audio_file.name}")
        print(f"  date={metadata['date']} time={metadata['time']}")
        print(f"  phone={metadata['phone']} direction={metadata['direction']}")


if __name__ == "__main__":
    main()