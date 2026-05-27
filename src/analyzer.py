TOP_JOBS = [
    "Комп'ютерна діагностика",
    "Заміна оливи ДВЗ + масляний фільтр",
    "Комплексна діагностика",
    "Ендоскопія",
]


def analyze_transcript(transcript: str) -> dict[str, object]:
    return {
        "call_summary": transcript[:120],
        "top_job": "",
        "manager_score": None,
        "comment": "",
        "flags": [],
    }