# Прогноз відтоку клієнтів

Цей проект дозволяє прогнозувати відтік клієнтів за допомогою Python, Dash і Docker.

## Зміст

1. [Передумови](#Передумови)
2. [Запуск за допомогою Docker Compose](#Запуск-за-допомогою-Docker-Compose)
3. [Альтернативний запуск через Dockerfile](#Альтернативний-запуск-через-Dockerfile)
4. [Основні команди](#Основні-команди)

---

## Передумови

Перед початком роботи переконайтеся, що на вашому комп'ютері встановлено:

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/)

---

## Запуск за допомогою Docker Compose

### 1. Клонування проекту
Склонуйте цей репозиторій на ваш локальний комп'ютер:
```bash
git clone https://github.com/MarkLewkowskii/Customer_Outflow.git
cd Customer_Outflow
```

### 2. Запуск з Docker Compose
Перейдіть у папку `docker` і виконайте команду для запуску:
```bash
cd docker
docker-compose up --build
```

### 3. Відкриття Dash-додатка
Відкрийте веб-браузер і перейдіть за адресою [http://localhost:8050](http://localhost:8050).

---

## Альтернативний запуск через Dockerfile

Якщо ви хочете запустити проект вручну через Dockerfile, виконайте наступні кроки:

### 1. Клонування проекту
Склонуйте цей репозиторій на ваш локальний комп'ютер:
```bash
git clone https://github.com/MarkLewkowskii/Customer_Outflow.git
cd Customer_Outflow
```

### 2. Збірка Docker-образу
Виконайте команду для створення Docker-образу:
```bash
docker build -t customer-outflow-model -f docker/Dockerfile .
```

### 3. Запуск контейнера
Запустіть контейнер з прив'язкою порту для Dash-додатка:
```bash
docker run -p 8050:8050 customer-outflow-model
```

### 4. Відкриття Dash-додатка
Відкрийте веб-браузер і перейдіть за адресою [http://localhost:8050](http://localhost:8050).

---

## Основні команди

### Перевірка доступних образів Docker
```bash
docker images
```

### Видалення контейнерів та образів
Очистіть контейнери та образи після завершення роботи:
```bash
docker system prune -f
```

### Перегляд логів контейнера
```bash
docker logs <container_id>
```

---

### Примітка

Якщо виникають помилки під час роботи з Docker або Dash, перевірте, чи правильно налаштовані шляхи у `Dockerfile`, `docker-compose.yml`, та у вашій локальній файловій системі.

