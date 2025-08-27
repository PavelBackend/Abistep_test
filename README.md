Описание:
Решил все-таки подключить базу, чтобы показать свою работу с FastAPI лучше.


Запуск:
# Клонируем репозиторий
git clone https://github.com/PavelBackend/Abistep_test.git

# Переходим в директорию проекта
cd Abistep_test

# Запускаем контейнеры
docker compose -f ./deploy/docker-compose.yml --env-file .env up --build -d

# Применяем миграции
docker compose -f ./deploy/docker-compose.yml exec app alembic -c api/alembic.ini upgrade head

http://localhost:8000/docs будет доступна документация

# Останавливаем контейнеры
docker compose -f ./deploy/docker-compose.yml down