from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

AUDIO_DIR = DATA_DIR / "audio"
INPUT_DIR = DATA_DIR / "input"
REFERENCE_DIR = DATA_DIR / "reference"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"

REPORT_PATH = INPUT_DIR / "report.xlsx"
OUTPUT_REPORT_PATH = OUTPUT_DIR / "report_filled.xlsx"