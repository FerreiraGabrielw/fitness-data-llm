import pandas as pd
from sqlalchemy import text
from etl.utils.db import get_engine
from etl.config.settings import CSV_PATH


def load_workout_exercises():
    engine = get_engine()

    # 1. Ler CSV
    df = pd.read_csv(CSV_PATH)

    # Parse datas
    df["start_time"] = pd.to_datetime(df["start_time"])
    df["end_time"] = pd.to_datetime(df["end_time"])

    # 2. Buscar mapeamento de workouts
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

    # 3. Gerar estrutura workout_exercises
    records = []
    seen = set()

    for (
        workout_name,
        start_time,
        end_time
    ), group in df.groupby(["title", "start_time", "end_time"]):

        workout_id = workouts_map.get((workout_name, start_time, end_time))
        if not workout_id:
            continue

        exercise_sequence = (
            group["exercise_title"]
            .drop_duplicates()
            .tolist()
        )

        for order, exercise_name in enumerate(exercise_sequence):
            exercise_id = exercises_map.get(exercise_name)
            if not exercise_id:
                continue

            superset_id = (
                group[group["exercise_title"] == exercise_name]["superset_id"]
                .dropna()
                .unique()
            )
            superset_id = int(superset_id[0]) if len(superset_id) > 0 else None

            key = (workout_id, exercise_id, order)
            if key in seen:
                continue
            seen.add(key)

            records.append({
                "workout_id": workout_id,
                "exercise_id": exercise_id,
                "exercise_order": order,
                "superset_id": superset_id,
                "notes": None
            })

    # 4. Inserção idempotente
    insert_sql = text("""
        INSERT INTO workout_exercises (
            workout_id,
            exercise_id,
            exercise_order,
            superset_id,
            notes
        )
        VALUES (
            :workout_id,
            :exercise_id,
            :exercise_order,
            :superset_id,
            :notes
        )
        ON CONFLICT DO NOTHING;
    """)

    with engine.begin() as conn:
        conn.execute(insert_sql, records)

    print(f"[OK] {len(records)} workout_exercises processed.")