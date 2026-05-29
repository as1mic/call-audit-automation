import re

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
    "хочу запис",
    "записатися",
    "записать",
    "на коли",
    "коли можна",
    "можна під'їхати",
    "можно подъехать",
    "можна до вас приїхати",
    "можна у вас приїхати",
    "приїхати на діагностику",
    "під'їхати завтра",
    "завтра на",
    "на 10 можна",
]

CAR_ALREADY_IN_SERVICE_KEYWORDS = [
    "авто в роботі",
    "машина у вас",
    "авто у вас",
    "завозив",
    "залишав",
    "оставлял",
    "привозив",
]

PROBLEM_KEYWORDS = [
    "не знаю",
    "не можу",
    "не підкажу",
    "передзвоніть",
    "зайняті",
    "немає місць",
]

GREETING_KEYWORDS = [
    "доброго дня",
    "добрий день",
    "добрый день",
    "вітаю",
]

GOODBYE_KEYWORDS = [
    "до побачення",
    "гарного дня",
    "дякую",
    "всього доброго",
]

BODY_KEYWORDS = [
    "кузов",
    "f30",
    "f25",
    "e70",
    "g30",
    "x3",
    "x5",
]

MILEAGE_KEYWORDS = [
    "пробіг",
    "пробег",
    "тисяч",
    "тысяч",
    "км",
]

PREVIOUS_REPAIR_KEYWORDS = [
    "робили раніше",
    "робилося раніше",
    "що робили",
    "що вже робили",
    "обслуговували",
]

PART_KEYWORDS = [
    "помпа",
    "фари",
    "бензобак",
    "масло",
    "олива",
    "фільтр",
    "радиатор",
    "радіатор",
    "амортизатор",
    "кнопка",
]

DIAGNOSTIC_KEYWORDS = [
    "комплексна діагностика",
    "комплексная диагностика",
    "діагностика",
    "диагностика",
]

JOB_KEYWORDS = {
    "Мийка / чистка деталі": [
        "чистка радіатора",
        "чистка радиатора",
        "честка радіатора",
        "чистите радіатор",
        "мийка",
        "мойка",
    ],
    "Комп'ютерна діагностика": [
        "комп'ютерна діагностика",
        "компьютерная диагностика",
        "комп діагностика",
    ],
    "Заміна оливи ДВЗ + масляний фільтр": [
        "заміна оливи",
        "заміна масла",
        "замена масла",
        "масляний фільтр",
        "масляный фильтр",
        "заміна мастил",
        "замена мастил",
        "то зробити",
        "то запис",
        "на то запис",
        "плану вто",
        "плану то",
        "заміна матла",
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
    "Заміна повітряного фільтра ДВЗ": [
        "повітряний фільтр",
        "воздушный фильтр",
    ],
    "Заміна фільтра салону в салонному відділенні": [
        "салонний фільтр",
        "салонный фильтр",
    ],
    "Заміна сайлентблоку": [
        "сайлентблок",
        "сайлентблоку",
    ],
    "Заміна амортизатора переднього": [
        "передній амортизатор",
        "передние амортизаторы",
        "амортизатор перед",
        "амортизаторам",
        "амортизатори",
    ],
    "Заміна амортизатора зд.": [
        "задній амортизатор",
        "задние амортизаторы",
        "амортизатор зад",
    ],
    "Заміна охолоджувальної рідини": [
        "охолоджувальна рідина",
        "антифриз",
    ],
    "Заміна гальмівної рідини з прокачкою": [
        "гальмівна рідина",
        "тормозная жидкость",
    ],
    "Заміна гальмівних дисків та колодок прд.": [
        "гальмівні диски",
        "тормозные диски",
        "колодки",
    ],
    "Заміна оливи АКПП": [
        "олива акпп",
        "масло акпп",
    ],
    "Зняття / встановлення повітряного патрубка": [
        "повітряний патрубок",
        "воздушный патрубок",
        "патрубок",
    ],
    "Кодування опцій": [
        "кодування",
        "кодирование",
    ],
}


def normalize_text(text: str) -> str:
    return " ".join(str(text).lower().split())


def has_any_keyword(text: str, keywords: list[str]) -> bool:
    normalized_text = normalize_text(text)

    for keyword in keywords:
        if normalize_text(keyword) in normalized_text:
            return True

    return False


def find_top_jobs_in_transcript(transcript: str) -> list[str]:
    transcript_text = normalize_text(transcript)
    matched_jobs = []

    for job in TOP_JOBS:
        if normalize_text(job) in transcript_text:
            matched_jobs.append(job)

    if matched_jobs:
        return matched_jobs

    for job_name, keywords in JOB_KEYWORDS.items():
        for keyword in keywords:
            if normalize_text(keyword) in transcript_text:
                matched_jobs.append(job_name)
                break

    return matched_jobs


def detect_booking(transcript: str) -> bool:
    return has_any_keyword(transcript, BOOKING_KEYWORDS)


def detect_booking_date(transcript: str, has_booking: bool) -> str:
    text = normalize_text(transcript)

    match = re.search(r"завтра на\s+(\d{1,2})", text)
    if match:
        hour = int(match.group(1))
        if 8 <= hour <= 20:
            return f"завтра {hour}:00"

    match = re.search(r"на\s+(\d{1,2})\s+можна", text)
    if match:
        hour = int(match.group(1))
        if 8 <= hour <= 20:
            return f"{hour}:00"

    if has_booking:
        return "не вказано"

    return ""


def detect_request_type(transcript: str) -> str:
    if has_any_keyword(transcript, CAR_ALREADY_IN_SERVICE_KEYWORDS):
        return "Авто в роботі"

    if detect_booking(transcript):
        return "Запис на сервіс"

    return "Консультація"


def detect_manager_name(transcript: str) -> str:
    match = re.search(r"менеджер\s+([а-яіїєґa-z]+)", normalize_text(transcript), re.IGNORECASE)
    if not match:
        return ""

    return match.group(1).capitalize()


def find_flags(transcript: str) -> list[str]:
    flags = []
    transcript_text = normalize_text(transcript)

    for keyword in PROBLEM_KEYWORDS:
        if normalize_text(keyword) in transcript_text:
            flags.append(keyword)

    return flags


def detect_greeting(transcript: str) -> int:
    return 1 if has_any_keyword(transcript, GREETING_KEYWORDS) else 0


def detect_body_question(transcript: str) -> int:
    return 1 if has_any_keyword(transcript, BODY_KEYWORDS) else 0


def detect_year_question(transcript: str) -> int:
    if re.search(r"\b(19|20)\d{2}\b", transcript):
        return 1

    return 1 if "рік" in normalize_text(transcript) or "год" in normalize_text(transcript) else 0


def detect_mileage_question(transcript: str) -> int:
    return 1 if has_any_keyword(transcript, MILEAGE_KEYWORDS) else 0


def detect_goodbye(transcript: str) -> int:
    return 1 if has_any_keyword(transcript, GOODBYE_KEYWORDS) else 0


def detect_diagnostic_offer(transcript: str) -> int:
    return 1 if has_any_keyword(transcript, DIAGNOSTIC_KEYWORDS) else 0


def detect_previous_repairs_question(transcript: str) -> int:
    return 1 if has_any_keyword(transcript, PREVIOUS_REPAIR_KEYWORDS) else 0


def detect_parts(transcript: str) -> str:
    parts = []
    transcript_text = normalize_text(transcript)

    for keyword in PART_KEYWORDS:
        if normalize_text(keyword) in transcript_text:
            parts.append(keyword)

    return ", ".join(parts[:3])


def detect_manager_issue(
    greeting_score: int,
    body_score: int,
    year_score: int,
    mileage_score: int,
    diagnostic_offer_score: int,
    previous_repairs_score: int,
    goodbye_score: int,
    top_job_ok: int,
    flags: list[str],
    has_booking: bool,
) -> bool:
    if body_score == 0:
        return True
    if mileage_score == 0:
        return True
    if top_job_ok == 0:
        return True
    return False


def build_comment(transcript: str) -> str:
    comment_parts = []
    flags = find_flags(transcript)

    if detect_booking(transcript):
        comment_parts.append("Клієнт цікавиться записом.")

    if flags:
        comment_parts.append(f"Проблемні моменти: {', '.join(flags)}.")

    return " ".join(comment_parts)


def analyze_transcript(transcript: str, metadata: dict) -> dict[str, object]:
    found_jobs = find_top_jobs_in_transcript(transcript)
    has_booking = detect_booking(transcript)
    flags = find_flags(transcript)
    top_job = found_jobs[0] if found_jobs else ""

    greeting_score = detect_greeting(transcript)
    body_score = detect_body_question(transcript)
    year_score = detect_year_question(transcript)
    mileage_score = detect_mileage_question(transcript)
    diagnostic_offer_score = detect_diagnostic_offer(transcript)
    previous_repairs_score = detect_previous_repairs_question(transcript)
    goodbye_score = detect_goodbye(transcript)
    top_job_ok = 1 if not flags else 0

    manager_score = (
        greeting_score
        + body_score
        + year_score
        + mileage_score
        + diagnostic_offer_score
        + previous_repairs_score
        + goodbye_score
        + top_job_ok
    )

    manager_issue = detect_manager_issue(
        greeting_score,
        body_score,
        year_score,
        mileage_score,
        diagnostic_offer_score,
        previous_repairs_score,
        goodbye_score,
        top_job_ok,
        flags,
        has_booking,
    )

    return {
        "call_summary": transcript[:120],
        "request_type": detect_request_type(transcript),
        "manager_name": detect_manager_name(transcript),
        "top_job": top_job,
        "has_booking": has_booking,
        "manager_score": manager_score,
        "booking_date": detect_booking_date(transcript, has_booking),
        "parts": detect_parts(transcript),
        "comment": build_comment(transcript),
        "flags": flags,
        "manager_issue": manager_issue,
        "score_total": manager_score,
        "score_max": 8,
        "greeting_score": greeting_score,
        "body_score": body_score,
        "year_score": year_score,
        "mileage_score": mileage_score,
        "diagnostic_offer_score": diagnostic_offer_score,
        "previous_repairs_score": previous_repairs_score,
        "goodbye_score": goodbye_score,
        "top_job_ok": top_job_ok,
    }