import pandas as pd
from sqlalchemy import text
from etl.utils.db import get_engine
from etl.config.settings import CSV_PATH


def load_workouts():
    engine = get_engine()

    # 1. Ler CSV
    df = pd.read_csv(CSV_PATH)

    # 2. Parse datas
    df["start_time"] = pd.to_datetime(df["start_time"])
    df["end_time"] = pd.to_datetime(df["end_time"])

    # 3. Agrupar por sessão de treino
    workouts = (
        df.groupby(["title", "start_time", "end_time"], as_index=False)
        .agg(
            workout_name=("title", "first"),
            description=("description", "first")
        )
    )

    # 4. Campos derivados
    workouts["workout_date"] = workouts["start_time"].dt.date
    workouts["duration_minutes"] = (
        (workouts["end_time"] - workouts["start_time"])
        .dt.total_seconds() / 60
    )
    workouts["source"] = "hevy_csv"

    # 5. SQLs
    select_sql = text("""
        SELECT workout_id
        FROM workouts
        WHERE workout_name = :workout_name
          AND start_time = :start_time
          AND end_time = :end_time
    """)

    insert_sql = text("""
        INSERT INTO workouts (
            workout_name,
            workout_date,
            start_time,
            end_time,
            duration_minutes,
            description,
            source
        )
        VALUES (
            :workout_name,
            :workout_date,
            :start_time,
            :end_time,
            :duration_minutes,
            :description,
            :source
        )
    """)

    inserted = 0

    with engine.begin() as conn:
        for _, row in workouts.iterrows():
            exists = conn.execute(
                select_sql,
                {
                    "workout_name": row["workout_name"],
                    "start_time": row["start_time"],
                    "end_time": row["end_time"],
                }
            ).fetchone()

            if exists:
                continue

            conn.execute(insert_sql, row.to_dict())
            inserted += 1

    print(f"[OK] {inserted} workouts inserted.")