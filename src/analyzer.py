from config import TOP_JOBS_PATH


def load_top_jobs() -> list[str]:
    jobs = []

    with open(TOP_JOBS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            job = line.strip()
            if job:
                jobs.append(job)

    return jobs


TOP_JOBS = load_top_jobs()

BOOKING_KEYWORDS = [
    "запис",
    "дата",
    "час",
    "коли вам зручно",
    "на сервіс",
    "підберемо час",
]

PROBLEM_KEYWORDS = [
    "не знаю",
    "не можу",
    "не підкажу",
    "передзвоніть",
    "зайняті",
    "немає місць",
]

GOOD_CONTACT_KEYWORDS = [
    "доброго дня",
    "дякую",
    "будь ласка",
]

ALL_KEYWORDS = {
    "booking": BOOKING_KEYWORDS,
    "problem": PROBLEM_KEYWORDS,
    "good_contact": GOOD_CONTACT_KEYWORDS,
}

JOB_KEYWORDS = {
    "Комп'ютерна діагностика": [
        "компютерна діагностика",
        "компьютерная диагностика",
        "комп діагностика",
        "комп диагностика",
    ],
    "Заміна оливи ДВЗ + масляний фільтр": [
        "заміна оливи",
        "заміна масла",
        "замена масла",
        "масляний фільтр",
        "масляный фильтр",
        "олива",
        "масло",
    ],
    "Комплексна діагностика": [
        "комплексна діагностика",
        "комплексная диагностика",
        "діагностика",
        "диагностика",
    ],
    "Ендоскопія": [
        "ендоскопія",
        "эндоскопия",
        "ендоскоп",
        "эндоскоп",
    ],
}


def normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def find_top_jobs_in_transcript(transcript: str) -> list[str]:
    found_jobs = []
    transcript_lower = normalize_text(transcript)

    for job in TOP_JOBS:
        if normalize_text(job) in transcript_lower:
            found_jobs.append(job)

    if found_jobs:
        return found_jobs

    for job_name, keywords in JOB_KEYWORDS.items():
        for keyword in keywords:
            if normalize_text(keyword) in transcript_lower:
                found_jobs.append(job_name)
                break

    return found_jobs


def analyze_transcript(transcript: str, metadata: dict) -> dict[str, object]:
    found_jobs = find_top_jobs_in_transcript(transcript)
    has_booking = detect_booking(transcript)
    flags = find_flags(transcript)
    comment = build_comment(transcript, metadata)

    return {
        "call_summary": transcript[:120],
        "top_job": found_jobs[0] if found_jobs else "",
        "has_booking": has_booking,
        "manager_score": None,
        "comment": comment,
        "flags": flags,
    }


def detect_booking(transcript: str) -> bool:
    transcript_lower = normalize_text(transcript)

    for keyword in BOOKING_KEYWORDS:
        if normalize_text(keyword) in transcript_lower:
            return True

    return False


def find_flags(transcript: str) -> list[str]:
    flags = []
    transcript_lower = normalize_text(transcript)

    for keyword in PROBLEM_KEYWORDS:
        if normalize_text(keyword) in transcript_lower:
            flags.append(keyword)

    return flags


def build_comment(transcript: str, metadata: dict) -> str:
    comment_parts = []

    if detect_booking(transcript):
        comment_parts.append("Клієнт цікавиться записом.")

    flags = find_flags(transcript)
    if flags:
        comment_parts.append(f"Проблемні моменти: {', '.join(flags)}.")

    return " ".join(comment_parts)