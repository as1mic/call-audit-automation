import os

from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"


AUDIO_DIR = DATA_DIR / "audio"
REFERENCE_DIR = DATA_DIR / "reference"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"


REPORT_PATH = BASE_DIR / "report.xlsx"
OUTPUT_REPORT_PATH = OUTPUT_DIR / "report_filled.xlsx"


CREDENTIALS_PATH = BASE_DIR / "credentials.json"
TOKEN_PATH = BASE_DIR / "token.json"


SOURCE_FOLDER_ID = os.getenv("SOURCE_FOLDER_ID", "")
TARGET_FOLDER_ID = os.getenv("TARGET_FOLDER_ID", "")


TOP_JOBS_PATH = REFERENCE_DIR / "top_jobs.txt"


ANALYZER_MODE = os.getenv("ANALYZER_MODE", "local").lower()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
