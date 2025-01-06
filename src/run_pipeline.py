import subprocess
import os

# Список скриптів для виконання
scripts = [
    "01_analyze_eda.py",
    "02_preprocessing.py",
    "03_model_training.py",
    "04_evaluation.py",
]

def execute_script(script_path):
    """Python-скрипт який запускає послідовно:
    "01_analyze_eda.py" - аналіз даних;
    "02_preprocessing.py" - підготовка даних;
    "03_model_training.py" - тренування моделі;
    "04_evaluation.py" - оцінка моделей;
    """
    try:
        print(f"Запуск {script_path}...")
        subprocess.run(["python", script_path], check=True)
        print(f"Завершено {script_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Під час виконання {script_path} сталася помилка: {e}")


# Визначення шляху до теки notebooks
notebooks_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../notebooks"))

if __name__ == "__main__":

    # Формування повного шляху до кожного скрипта та виконання
    for script in scripts:
        script_path = os.path.join(notebooks_dir, script)
        execute_script(script_path)

    print("Усі скрипти успішно виконано.")
