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


CREDENTIALS_PATH = BASE_DIR / "credentials.json"
TOKEN_PATH = BASE_DIR / "token.json"


SOURCE_FOLDER_ID = "1dpKG-eaFg2glOovkI4sYgLyPo3mW9Ilg"
TARGET_FOLDER_ID = "1rpiAWpJRbouG2X27KJVWlBmAkpHN2tA9"


TOP_JOBS_PATH = REFERENCE_DIR / "top_jobs.txt"
