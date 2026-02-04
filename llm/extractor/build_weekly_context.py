import json
import os
from datetime import date
from decimal import Decimal

from sqlalchemy import text
from etl.utils.db import get_engine

# ===============================
# CONFIG
# ===============================

OUTPUT_DIR = "llm/payloads"
SCHEMA_VERSION = "v1"


# ===============================
# UTILS
# ===============================

def json_safe(value):
    """
    Converte tipos não serializáveis (Decimal, date, datetime)
    para formatos compatíveis com JSON.
    """
    if isinstance(value, Decimal):
        return float(value)
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


# ===============================
# FETCH FUNCTIONS
# ===============================

def fetch_weekly_summary(conn, week_start):
    sql = text("""
        SELECT *
        FROM gold_weekly_fitness_summary
        WHERE week_start = :week_start
    """)
    row = conn.execute(
        sql,
        {"week_start": week_start}
    ).mappings().fetchone()

    return dict(row) if row else None


def fetch_exercise_context(conn, week_start):
    sql = text("""
        SELECT *
        FROM gold_llm_weekly_exercise_context_v1
        WHERE week_start = :week_start
        ORDER BY exercise_name
    """)

    rows = conn.execute(
        sql,
        {"week_start": week_start}
    ).mappings().fetchall()

    return [dict(r) for r in rows]


# ===============================
# PAYLOAD BUILDER
# ===============================

def build_payload(week_start: str):
    engine = get_engine()

    with engine.begin() as conn:
        weekly = fetch_weekly_summary(conn, week_start)
        if not weekly:
            raise RuntimeError(
                f"No weekly summary found for week_start={week_start}"
            )

        exercises_raw = fetch_exercise_context(conn, week_start)
        if not exercises_raw:
            raise RuntimeError(
                f"No exercise context found for week_start={week_start}"
            )

    # -------------------------------
    # Exercises
    # -------------------------------
    exercises = []

    for r in exercises_raw:
        exercises.append({
            "exercise_id": r["exercise_id"],
            "exercise_name": r["exercise_name"],
            "muscle_group": r["muscle_group_name"],

            "current_week": {
                "total_sets": r["current_total_sets"],
                "total_reps": r["current_total_reps"],
                "avg_reps": json_safe(r["current_avg_reps"]),
                "avg_weight_kg": json_safe(r["current_avg_weight_kg"]),
                "max_weight_kg": json_safe(r["current_max_weight_kg"]),
                "failure_sets": r["current_failure_sets"],
                "sessions_count": r["current_sessions"]
            },

            "delta_vs_last_week": {
                "total_sets": r["delta_sets"],
                "total_reps": r["delta_reps"],
                "avg_reps": json_safe(r["delta_avg_reps"]),
                "avg_weight_kg": json_safe(r["delta_avg_weight_kg"]),
                "max_weight_kg": json_safe(r["delta_max_weight_kg"]),
                "failure_sets": r["delta_failure_sets"]
            }
        })

    # -------------------------------
    # Final payload
    # -------------------------------
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": date.today().isoformat(),
        "week_start": weekly["week_start"].isoformat(),

        "cycle": {
            "cycle_name": weekly["cycle_name"],
            "cycle_type": weekly["cycle_type"]
        },

        "diet": {
            "avg_calories_kcal": json_safe(weekly["avg_calories_kcal"]),
            "avg_carbs_g": json_safe(weekly["avg_carbs_g"]),
            "avg_protein_g": json_safe(weekly["avg_protein_g"]),
            "avg_fat_g": json_safe(weekly["avg_fat_g"]),
            "cardio_weekly_min": weekly["cardio_weekly_min"],
            "avg_bodyweight_kg": json_safe(weekly["avg_bodyweight_kg"]),
            "logged_days": weekly["logged_days"]
        },

        "training_overview": {
            "training_sessions": weekly["training_sessions"],
            "total_sets": weekly["total_sets"],
            "failure_sets": weekly["failure_sets"],
            "avg_reps_per_set": json_safe(weekly["avg_reps_per_set"])
        },

        "exercises": exercises
    }

    return payload


# ===============================
# SAVE
# ===============================

def save_payload(payload):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fname = f"weekly_fitness_context_{payload['week_start']}.json"
    path = os.path.join(OUTPUT_DIR, fname)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return path


# ===============================
# MAIN
# ===============================

if __name__ == "__main__":
    # Use uma semana que você sabe que existe no banco
    WEEK_START = "2026-01-05"

    payload = build_payload(WEEK_START)
    path = save_payload(payload)

    print(f"[OK] Weekly context generated: {path}")
