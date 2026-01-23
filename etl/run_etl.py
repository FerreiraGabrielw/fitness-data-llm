from etl.load.load_exercises import load_exercises
from etl.load.load_workouts import load_workouts
from etl.load.load_workout_exercises import load_workout_exercises
from etl.load.load_sets import load_sets


def run():
    print("=== ETL STARTED ===")

    load_exercises()
    load_workouts()
    load_workout_exercises()
    load_sets()

    print("=== ETL FINISHED ===")


if __name__ == "__main__":
    run()