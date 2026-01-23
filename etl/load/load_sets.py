import pandas as pd
from sqlalchemy import text
from etl.utils.db import get_engine
from etl.config.settings import CSV_PATH


def clean_nan(value):
    """
    Converte NaN do pandas para None (NULL no PostgreSQL)
    """
    if pd.isna(value):
        return None
    return value


def load_sets():
    engine = get_engine()

    # 1. Ler CSV
    df = pd.read_csv(CSV_PATH)

    # Parse datas
    df["start_time"] = pd.to_datetime(df["start_time"])
    df["end_time"] = pd.to_datetime(df["end_time"])

    # 2. Mapas auxiliares
    with engine.begin() as conn:
        workouts_map = {
            (row.workout_name, row.start_time, row.end_time): row.workout_id
            for row in conn.execute(text("""
                SELECT workout_id, workout_name, start_time, end_time
                FROM workouts
            """))
        }

        exercises_map = {
            row.exercise_name: row.exercise_id
            for row in conn.execute(text("""
                SELECT exercise_id, exercise_name
                FROM exercises
            """))
        }

        workout_ex_map = {
            (row.workout_id, row.exercise_id, row.exercise_order): row.workout_exercise_id
            for row in conn.execute(text("""
                SELECT workout_exercise_id, workout_id, exercise_id, exercise_order
                FROM workout_exercises
            """))
        }

    inserted = 0

    insert_sql = text("""
        INSERT INTO sets (
            workout_exercise_id,
            set_index,
            set_type,
            weight_kg,
            reps,
            distance_km,
            duration_seconds,
            rpe
        )
        VALUES (
            :workout_exercise_id,
            :set_index,
            :set_type,
            :weight_kg,
            :reps,
            :distance_km,
            :duration_seconds,
            :rpe
        )
    """)

    exists_sql = text("""
        SELECT 1
        FROM sets
        WHERE workout_exercise_id = :workout_exercise_id
          AND set_index = :set_index
    """)

    with engine.begin() as conn:
        for (
            workout_name,
            start_time,
            end_time
        ), group in df.groupby(["title", "start_time", "end_time"]):

            workout_id = workouts_map.get((workout_name, start_time, end_time))
            if not workout_id:
                continue

            # Ordem dos exercícios dentro do treino
            exercise_sequence = (
                group["exercise_title"]
                .drop_duplicates()
                .tolist()
            )

            exercise_order_map = {
                name: idx for idx, name in enumerate(exercise_sequence)
            }

            for _, row in group.iterrows():
                exercise_id = exercises_map.get(row["exercise_title"])
                if not exercise_id:
                    continue

                exercise_order = exercise_order_map.get(row["exercise_title"])
                workout_exercise_id = workout_ex_map.get(
                    (workout_id, exercise_id, exercise_order)
                )

                if not workout_exercise_id:
                    continue

                exists = conn.execute(
                    exists_sql,
                    {
                        "workout_exercise_id": workout_exercise_id,
                        "set_index": int(row["set_index"]),
                    }
                ).fetchone()

                if exists:
                    continue

                conn.execute(
                    insert_sql,
                    {
                        "workout_exercise_id": workout_exercise_id,
                        "set_index": int(row["set_index"]),
                        "set_type": row["set_type"],
                        "weight_kg": clean_nan(row["weight_kg"]),
                        "reps": clean_nan(row["reps"]),
                        "distance_km": clean_nan(row["distance_km"]),
                        "duration_seconds": clean_nan(row["duration_seconds"]),
                        "rpe": clean_nan(row["rpe"]),
                    }
                )

                inserted += 1

    print(f"[OK] {inserted} sets inserted.")