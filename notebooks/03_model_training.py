# -*- coding: utf-8 -*-
"""03_model_training.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/MarkLewkowskii/Customer_Outflow/blob/main/notebooks/03_model_training.ipynb

# Розробка та навчання моделі
"""

import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from joblib import dump
# import winsound

"""Зчитування файлу processed_data.csv."""

df = pd.read_csv("data/processed/processed_data.csv")

"""Виділимо матриці X і y."""

X = df[df.columns[1:-1]]
y = df[df.columns[-1:]].values.flatten()

"""Розділимо дані на тренувальні та тестові."""

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=13
)

"""__Функція для виведення класифікаційного звіту__"""

def model_classification_report(model, model_name: str, X_test, y_test):
    y_pred = model.predict(X_test)
    print(
        f"Класифікаційний звіт для моделі {model_name}:\n",
        classification_report(y_test, y_pred),
    )

"""__Пошук параметрів за допомогою GridSearchCV__

**Задача:** Оптимізувати параметри для чотирьох моделей: *Random Forest*, *Histogram-based Gradient Boosting Classification Tree*, *Gradient Boosting* та *Logistic Regression*.

Усі ці алгоритми приймають велику кількість параметрів. Метод GridSearchCV перевіряє усі можливі комбінації параметрів із сітки. При збільшенні розмірів сітки кількість перевірок зростає з експоненційною швидкістю. Тому, оскільки прагнення до "ідеального" результату не завжди є раціональним, будемо застосовувати метод до малої групи параметрів, а не до всіх одразу. До того ж, за можливість, будемо зменшувати розмір сірки для конкретнних параметрів щоб точніше знайти діапазон з "ідеальним" параметром.

Для подальших досліджень було б доцільно автоматизувати цей процес, але поки такий підбір параметрів робиться вручну.

*Опис пошуку параметрів:*

Нехай є алгоритм $alg()$ з параметрами $p_1, p_2,...,p_n$.

1. Будуємо сітку для 2-3 параметрів. Наприклад, розглянемо сітку для параметрів $p_1, p_2, p_3$:
$$p_1: [a_1, b_1, c_1],$$
$$p_2: [a_2, b_2, c_2],$$
$$p_3: [a_3, b_3, c_3],$$
Серед цих параметрів обов'язково є параметри за замовчуванням.

2. Нехай у якості оптимальних параметрів було обрано $p_{1 opt}=a_1, p_{2 opt}=b_2, p_{3 opt}=c_3$. Якщо це можливо, то змешнуємо діапазон сітки для пошуку більш оптимальних параметрів. Наприклад, тепер розглядаємо наступну сітку:
$$p_1: [d_1, p_{1 opt}, e_1],$$
$$p_2: [d_2, p_{2 opt}, e_2],$$
$$p_3: [d_3, p_{3 opt}, e_3],$$
де
$$d_1<p_{1 opt}=a_1<e_1<b_1,$$
$$a_2<d_2<p_{2 opt}=b_2<e_2<c_2,$$
$$b_3<d_3<p_{3 opt}=c_3<e_3.$$
Повторюємо цей процес доти поки ріст точності не зупинеться.

3. Нехай у якості оптимальних параметрів було обрано $p_{1 opt}, p_{2 opt}, p_{3 opt}$, причому, наприклад, $p_{1 opt}$ є параметром за замовчуванням. Далі повторюємо кроки **1**, **2** для алготитму $alg(p_2=p_{2 opt}, p_3=p_{3 opt})$ для наступної групи параметрів. Наприклад, можна розглянути сітку для параметрів $p_3, p_4$.

4. Робимо кроки **1**-**3** поки не перевіримо усі параметри.

__Функція для пошуку параметрів за допомогою GridSearchCV__
"""

def grid_search_fun(alg, param_grid, X, y):
    grid_search = GridSearchCV(
        alg,
        param_grid,
        scoring="accuracy",
        cv=3,
    )

    grid_search.fit(X, y)

    print("Найкращі параметри:", grid_search.best_params_)
    print("Найкраще значення точності:", grid_search.best_score_)

"""__Пошук параметрів за допомогою GridSearchCV для алгоритму Random Forest__"""

param_grid_RF = {
    # "n_estimators": [100, 101, 99],  # Кількість дерев
    # "criterion": ["gini", "log_loss", "entropy"],  # Функція для оцінки поділу
    # "max_depth": [1, 2, None],  # Глибина дерева
    # "min_samples_split": [2, 3],  # Мінімальна кількість зразків для поділу
    # "min_samples_leaf": [1, 2, 3],  # Мінімальна кількість зразків у листі
    # "min_weight_fraction_leaf": [
    #     0.0,
    #     0.1,
    #     0.2,
    # ],  # Мінімальна частка ваги зразків у листі
    # "max_features": [
    #     "sqrt",
    #     "log2",
    #     None,
    # ],  # Кількість ознак, що розглядаються для поділу
    # "max_leaf_nodes": [None, 2, 3, 5],  # Максимальна кількість вузлів у дереві
    # "min_impurity_decrease": [
    #     0.0,
    #     0.01,
    #     0.1,
    # ],  # Мінімальне зменшення показника невизначеності
    # "bootstrap": [True, False],  # Використання бутстрепінгу
    # "oob_score": [False, True],  # Використання зразків поза мішком для оцінки
    # "warm_start": [False, True],
    # "ccp_alpha": [0.0, 0.01, 0.1],  # Параметр для пост-підрізання дерева
    # "max_samples": [
    #     None,
    #     0.1,
    #     0.5,
    # ],  # Частка зразків, що використовуються для навчання кожного дерева
}

GrS_RF = 0
if GrS_RF:
    grid_search_fun(
        RandomForestClassifier(
            # n_estimators=161,
            # criterion="log_loss",
            max_depth=2,
            # min_samples_split=4
            min_samples_leaf=2,
            # min_weight_fraction_leaf=0.1,
            max_features=None,
            # random_state=13,
        ),
        param_grid_RF,
        X,
        y,
    )
    winsound.MessageBeep()  # Повідомляє вголос, що пошук завершено.

"""__Модель Random Forest__"""

model_RF = RandomForestClassifier(
    n_estimators=161,
    criterion="log_loss",
    min_samples_leaf=2,
    max_features=None,
)

"""Навчання моделі Random Forest."""

model_RF.fit(X_train, y_train)

model_classification_report(model_RF, "Random Forest", X_test, y_test)

"""Збережемо модель у файл."""

dump(model_RF, "models/model_RandomForest.joblib")

"""__Пошук параметрів за допомогою GridSearchCV для алгоритму Histogram-based Gradient Boosting Classification Tree__"""

param_grid_HGB = {
    # "learning_rate": [0.09, 0.1, 0.2],  # Швидкість навчання
    # "max_iter": [260, 261, 262],  # Кількість ітерацій
    # "max_leaf_nodes": [31, 65, 66, 67],
    # "max_depth": [None, 5, 10],  # Максимальна глибина дерева
    # "min_samples_leaf": [9, 10, 11],  # Мінімальна кількість зразків у листі
    # "l2_regularization": [0.0, 2.5, 2.6, 2.7],  # L2-регуляризація
    # "max_bins": [128, 255, 300],  # Кількість бінів
    # "interaction_cst": [None, "pairwise", "no_interactions"],
    # "warm_start": [False, True],
    # "early_stopping": [True, False, "auto"],  # Чи використовувати ранню зупинку
    # "scoring": [None, "accuracy", "roc_auc", "loss"],  # Метрика для ранньої зупинки
    # "n_iter_no_change": [1, 2, 10],  # Кількість ітерацій без покращення для зупинки
    # "tol": [1e-10, 1e-9, 1e-8, 1e-7],  # Точність для критерію зупинки
    # "class_weight": ["balanced", None],
}

GrS_HGB = 0
if GrS_HGB:
    grid_search_fun(
        HistGradientBoostingClassifier(
            # learning_rate=0.1,
            max_iter=261,
            max_leaf_nodes=66,
            # max_depth=None,
            min_samples_leaf=10,
            l2_regularization=2.5,
            # max_bins=255,
            # interaction_cst=None,
            # warm_start=False,
            early_stopping=False,
            scoring=None,
            # n_iter_no_change=5,
            # tol=1e-07,
            # class_weight=None,
        ),
        param_grid_HGB,
        X,
        y,
    )
    winsound.MessageBeep()  # Повідомляє вголос, що пошук завершено.

"""__Модель Histogram-based Gradient Boosting Classification Tree__"""

model_HGB = HistGradientBoostingClassifier(
    max_iter=261,
    max_leaf_nodes=66,
    min_samples_leaf=10,
    l2_regularization=2.5,
    early_stopping=False,
    scoring=None,
)

"""Навчання моделі Histogram-based Gradient Boosting."""

model_HGB.fit(X_train, y_train)

model_classification_report(
    model_HGB, "Histogram-based Gradient Boosting Classification Tree", X_test, y_test
)

"""Збережемо модель у файл."""

dump(model_HGB, "models/model_HistGradientBoosting.joblib")

"""__Пошук параметрів за допомогою GridSearchCV для алгоритму Gradient Boosting__"""

param_grid_GB = {
    # "loss": ["log_loss", "exponential"],  # Функція втрат
    # "learning_rate": [0.2, 0.3, 0.4],  # Швидкість навчання
    # "n_estimators": [504, 505, 506, 509],  # Кількість дерев
    # "subsample": [0.8, 0.9, 1.0],  # Частка вибірки для кожного дерева
    # "criterion": ["friedman_mse", "squared_error"],  # Критерій для розбиття
    # "min_samples_split": [2, 3, 4],  # Мінімальна кількість зразків для розбиття вузла
    # "min_samples_leaf": [1, 2, 3],  # Мінімальна кількість зразків у листовому вузлі
    # "min_weight_fraction_leaf": [0.0, 0.1, 0.2],
    # "max_depth": [3, None,  4, 5],  # Максимальна глибина дерева
    # "min_impurity_decrease": [
    #     0.0,
    #     0.1,
    #     1.0,
    #     10.0,
    # ],  # Мінімальне зменшення impurity для розбиття
    # "max_features": [None, "sqrt", "log2"],  # Кількість фіч для кожного дерева
    # "max_leaf_nodes": [None, 2, 3],
    # "warm_start": [False, True],
    # "n_iter_no_change": [None, 1, 2],
    # "tol": [1e-4, 1e-5, 1e-3],
    # "ccp_alpha": [0.0, 0.1, 0.2],
}

GrS_GB = 0
if GrS_GB:
    grid_search_fun(
        GradientBoostingClassifier(
            learning_rate=0.2, n_estimators=505, criterion="squared_error", warm_start=True
        ),
        param_grid_GB,
        X,
        y,
    )
    winsound.MessageBeep()  # Повідомляє вголос, що пошук завершено.

"""__Модель Gradient Boosting__"""

model_GB = GradientBoostingClassifier(
    learning_rate=0.2, n_estimators=505, criterion="squared_error", warm_start=True
)

"""Навчання моделі Gradient Boosting."""

model_GB.fit(X_train, y_train)

model_classification_report(model_GB, "Gradient Boosting", X_test, y_test)

"""Збережемо модель у файл."""

dump(model_GB, "models/model_GradientBoosting.joblib")

"""__Пошук параметрів за допомогою GridSearchCV для алгоритму Logistic Regression__"""

param_grid_LR = {
    # "penalty": [
    #     "l2",
    #     # "l1",
    #     # None,
    # ],  # Тип регуляризації
    # "solver": [
    #     # "newton-cg",
    #     # "newton-cholesky",
    #     # "lbfgs",
    #     "liblinear",
    #     # "sag",
    #     # "saga",
    # ],  # Алгоритми оптимізації
    # "tol": [1e-4, 1e-2, 1e-1],  # Допустима похибка для зупинки
    # "C": [1.0, 16, 19, 20, 21, 30],  # Інверсія сили регуляризації
    # "fit_intercept": [True, False],  # Чи включати в модель константу
    # "max_iter": [165, 166, 169],  # Максимальна кількість ітерацій
    # "intercept_scaling": [
    #     1,
    #     10,
    #     100,
    # ],  # Масштаб інтерсепта (активний для solver='liblinear')
}

GrS_LR = 0
if GrS_LR:
    grid_search_fun(
        LogisticRegression(penalty="l2", solver="saga", tol=1e-2, C=16, max_iter=165),
        param_grid_LR,
        X,
        y,
    )
    winsound.MessageBeep()  # Повідомляє вголос, що пошук завершено.

"""__Модель Logistic Regression__"""

model_LR = LogisticRegression(penalty="l2", solver="saga", tol=1e-2, C=16, max_iter=165)

"""Навчання моделі Logistic Regression."""

model_LR.fit(X_train, y_train)

model_classification_report(model_LR, "Logistic Regression", X_test, y_test)

"""Збережемо модель у файл."""

dump(model_LR, "models/model_LogisticRegression.joblib")

"""__Висновки__

Розглянуто чотири моделі з бібліотеки `sklearn`. Здійснено оцінку *точності* моделей на тестових даних за допомогою `classification_report`.

Моделі *Random Forest* та *Histogram-based Gradient Boosting Classification Tree* показали однакові значення метрик якості. Метод *Gradient Boosting* має трохи нижчі значення метрик якості. Модель *Logistic Regression* має відчутно меншу точність ніж усі інші, але однаково залишається досить точною.

Маємо наступний рейтинг моделей (починаючи від найточнішої):

1. *Random Forest*, *Histogram-based Gradient Boosting Classification Tree*
2. *Gradient Boosting*
3. *Logistic Regression*

Отже, на тестових даних найкраще себе показали моделі *Random Forest* та *Histogram-based Gradient Boosting Classification Tree*.
"""