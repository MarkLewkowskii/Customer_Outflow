import json
import matplotlib.pyplot as plt
import os



class ModelEvaluationVisualizer:
    """
    Модуль для візуалізації данних на основі основних результатів навчальних моделій. Цей модуль будує порівняльні графіки.
    """

    def __init__(self, base_dir, results_dir="results", json_filename="model_evaluation.json"):
        self.results_dir = os.path.join(base_dir, results_dir)
        self.json_file_path = os.path.join(self.results_dir, json_filename)

        # Перевіряємо, чи файл існує
        if not os.path.exists(self.json_file_path):
            raise FileNotFoundError(f"Файл {self.json_file_path} не знайдено. Перевірте шлях.")

        # Створюємо папку для результатів, якщо її немає
        os.makedirs(self.results_dir, exist_ok=True)

        # Завантаження даних з JSON
        with open(self.json_file_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def parse_data(self):
        model_names = []
        accuracies = []
        f1_scores = []
        model_sizes = []

        # Отримуємо дані з JSON
        for model_name, model_data in self.data.items():
            model_names.append(model_name)
            accuracies.append(model_data["classification_report"]["accuracy"] * 100)  # Точність у відсотках
            f1_scores.append(model_data["classification_report"]["macro avg"]["f1-score"] * 100)  # F1-метрика
            model_sizes.append(model_data["model_size_mb"])  # Розмір моделі в MB

        return model_names, accuracies, f1_scores, model_sizes

    def create_plots(self):
        model_names, accuracies, f1_scores, model_sizes = self.parse_data()

        # Побудова графіку точності
        plt.figure(figsize=(10, 6))
        plt.bar(model_names, accuracies, color="skyblue")
        plt.title("Точність моделей", fontsize=14)
        plt.ylabel("Точність (%)", fontsize=12)
        plt.xlabel("Моделі", fontsize=12)
        plt.xticks(rotation=15, fontsize=10)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, "accuracy_comparison.png"))

        # Побудова графіку F1-score
        plt.figure(figsize=(10, 6))
        plt.bar(model_names, f1_scores, color="green")
        plt.title("F1-метрика моделей", fontsize=14)
        plt.ylabel("F1-метрика (%)", fontsize=12)
        plt.xlabel("Моделі", fontsize=12)
        plt.xticks(rotation=15, fontsize=10)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, "f1_score_comparison.png"))

        # Побудова графіку розмірів моделей
        plt.figure(figsize=(10, 6))
        plt.bar(model_names, model_sizes, color="orange")
        plt.title("Розмір моделей", fontsize=14)
        plt.ylabel("Розмір (MB)", fontsize=12)
        plt.xlabel("Моделі", fontsize=12)
        plt.xticks(rotation=15, fontsize=10)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.results_dir, "model_size_comparison.png"))

        print("Графіки успішно збережені в папці results.")


if __name__ == "__main__":
    # Отримуємо абсолютний шлях до кореневої директорії проекту
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Створюємо візуалізатор
    visualizer = ModelEvaluationVisualizer(BASE_DIR)
    visualizer.create_plots()
