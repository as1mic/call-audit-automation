# Call audit automation

Small script for the test task. It takes audio files from Google Drive, copies them to a working Drive folder, transcribes them and then fills an Excel report with call analysis.

By default everything works locally: transcription is done with faster-whisper, and call analysis is done with simple rules and keywords. I also added an optional OpenAI API mode, mostly to check if the local analysis is the weak part or the transcript itself is bad.

## Before running

1. Put `credentials.json` in the project root.
2. Create `.env` from `.env.example` and set Google Drive folder ids there.
3. Put the source spreadsheet in the project root and name it `report.xlsx`.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
py src/main.py
```

On the first run Google auth will open in the browser. After that `token.json` is created and the script will reuse it.

The filled report is saved here:

```text
output/report_filled.xlsx
```

Transcripts are saved locally in `data/transcripts`, and also uploaded to the working Google Drive folder next to the audio files.

## OpenAI mode

Default mode:

```env
ANALYZER_MODE=local
```

If API analysis is needed, create `.env` and add:

```env
OPENAI_API_KEY=your_key
ANALYZER_MODE=openai
OPENAI_MODEL=gpt-4o-mini
```

Local mode is free and does not need any API key. OpenAI mode is more flexible with messy transcripts and natural language, but it uses API credits.

## Note

`credentials.json`, `token.json`, `.env`, audio files, transcripts and generated reports are not committed to the repository because they may contain private data.