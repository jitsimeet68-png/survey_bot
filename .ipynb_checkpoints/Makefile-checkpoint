.PHONY: up down restart logs build clean ps db-shell bot-shell

# Запуск всех сервисов
up:
	docker compose up -d

# Остановка всех сервисов
down:
	docker compose down

# Перезапуск
restart:
	docker compose restart

# Просмотр логов
logs:
	docker compose logs -f

# Пересборка контейнеров
build:
	docker compose build --no-cache

# Очистка (включая volumes)
clean:
	docker compose down -v
	docker system prune -f

# Статус сервисов
ps:
	docker compose ps

# Подключение к PostgreSQL
db-shell:
	docker compose exec postgres psql -U postgres -d survey_bot

# Подключение к контейнеру бота
bot-shell:
	docker compose exec bot /bin/bash

# Только бот
bot-up:
	docker compose up -d bot

bot-restart:
	docker compose restart bot

bot-logs:
	docker compose logs -f bot

# NocoDB
noco-restart:
	docker compose restart nocodb

noco-logs:
	docker compose logs -f nocodb