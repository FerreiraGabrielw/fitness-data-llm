from etl.load.load_exercises import load_exercises


def run():
    print("=== ETL STARTED ===")
    load_exercises()
    print("=== ETL FINISHED ===")


if __name__ == "__main__":
    run()
