# Агрегатор погодных данных — г. Сочи

Контрольная работа по дисциплине: АДМ, СОПР. и DevOps
Вариант 3 — Агрегатор погодных данных
Студент: Антонов Н.В., группа ИВТ-460

## Описание

Система сбора, нормализации и визуализации данных о погоде из двух источников:
- **Open-Meteo API** — реальный открытый REST-сервис (без ключа)
- **Gismeteo** — эмуляция через генерацию данных

Данные нормализуются к единой схеме и сохраняются в MySQL 8.0.

## Компоненты

| Сервис | Технология | Порт |
|---|---|---|
| База данных | MySQL 8.0 | 3306 |
| Администрирование БД | phpMyAdmin | 8080 |
| Визуализация | Metabase | 3001 |
| Веб-приложение | Flask | — |
| Reverse Proxy | Nginx | 80 |
| Парсер | Python + requests | — |

## Запуск

git clone https://github.com/oxknx33-hub/weather-sochi.git
cd weather-sochi
docker compose up -d --build

Открыть в браузере: http://localhost

## Страницы

- http://localhost — главная страница
- http://localhost/data — данные JSON
- http://localhost:8080 — phpMyAdmin
- http://localhost:3001 — Metabase

## CI/CD

Автоматическая проверка кода при каждом push через GitHub Actions (flake8).
