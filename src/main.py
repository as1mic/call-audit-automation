from config import SOURCE_FOLDER_ID, TARGET_FOLDER_ID, AUDIO_DIR, TRANSCRIPTS_DIR, REPORT_PATH, OUTPUT_REPORT_PATH, ANALYZER_MODE
from excel_writer import load_report, save_report, get_main_sheet, get_or_create_row, prepare_report_sheet, write_analysis_to_row
from google_drive import get_drive_service, list_files_in_folder, filter_audio_files, get_existing_file_names, copy_file_to_folder, download_file, upload_file_to_folder
from transcribe import get_audio_files, parse_audio_filename, get_transcription_model, transcribe_audio, save_transcript
from analyzer import analyze_transcript


def analyze_call(transcript_text: str, metadata: dict) -> dict[str, object]:
    if ANALYZER_MODE == "openai":
        from openai_analyzer import analyze_transcript_with_openai
        return analyze_transcript_with_openai(transcript_text, metadata)
    return analyze_transcript(transcript_text, metadata)


def main() -> None:
    drive_service = get_drive_service()
    if drive_service:
        print("Connected to Google Drive")
        print(f"Analyzer mode: {ANALYZER_MODE}")
    else:
        print("Failed to connect to Google Drive")
        return

    drive_files = list_files_in_folder(drive_service, SOURCE_FOLDER_ID)
    print(f"Found {len(drive_files)} files in source folder")

    audio_files = filter_audio_files(drive_files)
    if audio_files:
        print(f"Found {len(audio_files)} audio files")
    else:
        print("No audio files found")
        return

    existing_names = get_existing_file_names(drive_service, TARGET_FOLDER_ID)
    print(f"Files already in target folder: {len(existing_names)}")

    copied_count = 0
    skipped_count = 0

    for audio_file in audio_files:
        file_name = audio_file["name"]

        if file_name in existing_names:
            print(f"Skipped {file_name} (already in target)")
            skipped_count += 1
            continue

        copy_file_to_folder(
            drive_service,
            audio_file["id"],
            TARGET_FOLDER_ID,
            file_name,
        )
        existing_names.add(file_name)
        copied_count += 1
        print(f"Copied {file_name}")

    print(f"Copy summary: {copied_count} copied, {skipped_count} skipped")

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    downloaded_count = 0
    download_skipped_count = 0

    for audio_file in audio_files:
        file_name = audio_file["name"]
        local_path = AUDIO_DIR / file_name

        if local_path.exists():
            print(f"Skipped {file_name} (already downloaded)")
            download_skipped_count += 1
            continue

        download_file(drive_service, audio_file["id"], local_path)
        downloaded_count += 1
        print(f"Downloaded {file_name}")

    print(f"Download summary: {downloaded_count} downloaded, {download_skipped_count} skipped")

    local_audio_files = get_audio_files(AUDIO_DIR)
    print(f"Local audio files: {len(local_audio_files)}")

    if not local_audio_files:
        print("No local audio files for transcription")
        return

    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    model = get_transcription_model()

    transcribed_count = 0
    transcription_skipped_count = 0

    for audio_path in local_audio_files:
        transcript_path = TRANSCRIPTS_DIR / f"{audio_path.stem}.txt"

        if transcript_path.exists():
            print(f"Skipped transcription for {audio_path.name} (already exists)")
            transcription_skipped_count += 1
            continue

        transcript_text = transcribe_audio(model, audio_path)
        save_transcript(audio_path, transcript_text)
        transcribed_count += 1
        print(f"Transcribed {audio_path.name}")

    print(f"Transcription summary: {transcribed_count} transcribed, {transcription_skipped_count} skipped")

    target_names = get_existing_file_names(drive_service, TARGET_FOLDER_ID)
    uploaded_transcripts_count = 0
    skipped_transcripts_count = 0

    for transcript_path in sorted(TRANSCRIPTS_DIR.glob("*.txt")):
        if transcript_path.name in target_names:
            print(f"Skipped {transcript_path.name} (already in target)")
            skipped_transcripts_count += 1
            continue

        upload_file_to_folder(drive_service, transcript_path, TARGET_FOLDER_ID)
        target_names.add(transcript_path.name)
        uploaded_transcripts_count += 1
        print(f"Uploaded {transcript_path.name}")

    print(f"Upload summary: {uploaded_transcripts_count} uploaded, {skipped_transcripts_count} skipped")

    analyzed_count = 0

    workbook = load_report(REPORT_PATH)
    sheet = get_main_sheet(workbook)
    prepare_report_sheet(sheet)

    for audio_path in local_audio_files:
        transcript_path = TRANSCRIPTS_DIR / f"{audio_path.stem}.txt"

        if not transcript_path.exists():
            print(f"Warning: transcript not found for {audio_path.name}")
            continue

        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript_text = f.read().strip()

        metadata = parse_audio_filename(audio_path.name)
        analysis_result = analyze_call(transcript_text, metadata)
        row_number = get_or_create_row(sheet, metadata)

        write_analysis_to_row(sheet, row_number, metadata, analysis_result)
        analyzed_count += 1

        print(f"Analyzed {audio_path.name}")

    saved_report_path = save_report(workbook, OUTPUT_REPORT_PATH)
    print(f"Report saved to {saved_report_path}")
    print(f"Total analyzed: {analyzed_count}")


if __name__ == "__main__":
    main()