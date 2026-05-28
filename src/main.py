from config import SOURCE_FOLDER_ID, TARGET_FOLDER_ID, AUDIO_DIR, TRANSCRIPTS_DIR, REPORT_PATH
from excel_writer import load_report, find_row_by_date, get_main_sheet
from google_drive import get_drive_service, list_files_in_folder, filter_audio_files, get_existing_file_names, copy_file_to_folder, download_file
from transcribe import get_audio_files, parse_audio_filename, get_transcription_model, transcribe_audio, save_transcript
from analyzer import analyze_transcript

def main() -> None:
    drive_service = get_drive_service()
    if drive_service:
        print("Connected to Google Drive")
    else:
        print("Could not connect to Google Drive")
        return

    drive_files = list_files_in_folder(drive_service, SOURCE_FOLDER_ID)
    print(f"Found {len(drive_files)} files in the source folder")

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
            print(f"{audio_file['name']} is already in the target folder")
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
        print(f"Copied {file_name} to the target folder")

    print(f"Copied: {copied_count}")
    print(f"Skipped: {skipped_count}")

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    downloaded_count = 0
    download_skipped_count = 0

    for audio_file in audio_files:
        file_name = audio_file["name"]
        local_path = AUDIO_DIR / file_name

        if local_path.exists():
            print(f"{file_name} is already downloaded")
            download_skipped_count += 1
            continue

        download_file(drive_service, audio_file["id"], local_path)
        downloaded_count += 1
        print(f"Downloaded {file_name}")

    print(f"Downloaded files: {downloaded_count}")
    print(f"Already local: {download_skipped_count}")

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
            print(f"Transcript for {audio_path.name} already exists")
            transcription_skipped_count += 1
            continue

        transcript_text = transcribe_audio(model, audio_path)
        save_transcript(audio_path, transcript_text)
        transcribed_count += 1
        print(f"Saved transcript for {audio_path.name}")

    print(f"Transcribed files: {transcribed_count}")
    print(f"Skipped by existing transcripts: {transcription_skipped_count}")

    analyzed_count = 0

    workbook = load_report(REPORT_PATH)
    sheet = get_main_sheet(workbook)

    for audio_path in local_audio_files:
        transcript_path = TRANSCRIPTS_DIR / f"{audio_path.stem}.txt"

        if not transcript_path.exists():
            print(f"Transcript not found for {audio_path.name}")
            continue

        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript_text = f.read().strip()

        metadata = parse_audio_filename(audio_path.name)
        analysis_result = analyze_transcript(transcript_text, metadata)
        row_number = find_row_by_date(sheet, metadata["date"])

        if row_number == -1:
            print(f"No row found for {audio_path.name} with date {metadata['date']}")
            continue

        print(f"Found row {row_number} for {audio_path.name}")

        analyzed_count += 1

        print(f"Analysis for {audio_path.name}")
        print(f"top_job: {analysis_result['top_job']}")
        print(f"has_booking: {analysis_result['has_booking']}")
        print(f"flags: {analysis_result['flags']}")
        print(f"comment: {analysis_result['comment']}")
        print(f"summary: {analysis_result['call_summary']}")

    print(f"Analyzed transcripts: {analyzed_count}")

if __name__ == "__main__":
    main()
