import pandas as pd
from sqlalchemy import text
from etl.utils.db import get_engine
from etl.config.settings import CSV_PATH


def load_exercises():
    engine = get_engine()

    # 1. Ler CSV (Bronze → memória)
    df = pd.read_csv(CSV_PATH)

    # 2. Extrair exercícios únicos
    exercises = (
        df["exercise_title"]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .to_frame(name="exercise_name")
    )

    # 3. Inferir se é cardio
    cardio_mask = (
        df.groupby("exercise_title")[["distance_km", "duration_seconds"]]
        .apply(lambda x: x.notna().any().any())
    )

    exercises["is_cardio"] = (
        exercises["exercise_name"]
        .map(cardio_mask)
        .fillna(False)
    )

    # 4. Inserção idempotente
    insert_sql = text("""
        INSERT INTO exercises (exercise_name, is_cardio)
        VALUES (:exercise_name, :is_cardio)
        ON CONFLICT (exercise_name) DO NOTHING;
    """)

    with engine.begin() as conn:
        conn.execute(
            insert_sql,
            exercises.to_dict(orient="records")
        )

    print(f"[OK] {len(exercises)} exercises processed.")