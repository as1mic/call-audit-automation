import json

from openai import OpenAI

from analyzer import TOP_JOBS
from config import OPENAI_MODEL


SCORE_FIELDS = [
    "greeting_score",
    "body_score",
    "year_score",
    "mileage_score",
    "diagnostic_offer_score",
    "previous_repairs_score",
    "goodbye_score",
    "top_job_ok",
]


def build_prompt(transcript: str, metadata: dict) -> str:
    top_jobs_text = "\n".join(f"- {job}" for job in TOP_JOBS)

    return f"""
Analyze this car service call transcript and return only JSON.

Available top jobs:
{top_jobs_text}

Return JSON with these fields:
request_type, manager_name, top_job, has_booking, flags, comment, manager_issue,
score_total, score_max,
greeting_score, body_score, year_score, mileage_score,
diagnostic_offer_score, previous_repairs_score, goodbye_score, top_job_ok,
booking_date, parts.

Rules:
- request_type: "Авто в роботі", "Запис на сервіс" or "Консультація".
- top_job must be from the available top jobs list, or empty string.
- scores must be 1 or 0.
- flags must be short problem phrases.
- booking_date can be empty if no appointment date is clear.
- parts can be empty if no parts are clear.
- comment must be short Ukrainian text, describing the call or problems found.
- manager_issue: true if there is a problem with manager's work (didn't ask about car model/body, didn't ask about mileage, didn't offer diagnostic, there are problem flags, poor goodbye), false otherwise.
- score_total: sum of all binary scores (0-8).
- score_max: maximum possible score (8).

Date: {metadata.get("date", "")}
Phone: {metadata.get("phone", "")}
Direction: {metadata.get("direction", "")}

Transcript:
{transcript}
""".strip()


def calculate_manager_score(result: dict) -> int:
    total = 0

    for field in SCORE_FIELDS:
        value = result.get(field, 0)
        total += int(value)

    return total


def analyze_transcript_with_openai(transcript: str, metadata: dict) -> dict[str, object]:
    client = OpenAI()

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=build_prompt(transcript, metadata),
        text={"format": {"type": "json_object"}},
    )

    result = json.loads(response.output_text)
    result["call_summary"] = transcript[:120]
    result["manager_score"] = calculate_manager_score(result)

    if "flags" not in result:
        result["flags"] = []

    if "comment" not in result:
        result["comment"] = ""

    if "booking_date" not in result:
        result["booking_date"] = ""

    if "parts" not in result:
        result["parts"] = ""

    if "manager_issue" not in result:
        result["manager_issue"] = False

    if "score_total" not in result:
        result["score_total"] = result.get("manager_score", 0)

    if "score_max" not in result:
        result["score_max"] = 8

    return result