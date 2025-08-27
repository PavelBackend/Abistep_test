Описание:
Не смотря на то, что это было необязательно - подключил базу, чтобы показать свою работу с FastAPI и его окружением лучше.
- Операция перевода поддерживает точность до 2 знаков после запятой
- Убрал .env из .gitignore для легкого запуска тестового


Запуск:
# Клонируем репозиторий
git clone https://github.com/PavelBackend/Abistep_test.git

# Переходим в директорию проекта
cd Abistep_test

# Запускаем контейнеры
docker compose -f ./deploy/docker-compose.yml --env-file .env up --build -d

# Применяем миграции
docker compose -f ./deploy/docker-compose.yml exec main_service alembic -c api/alembic.ini upgrade head

http://localhost:8000/docs будет доступна документация

# Останавливаем контейнеры
docker compose -f ./deploy/docker-compose.yml down
