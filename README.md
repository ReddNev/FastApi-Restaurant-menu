# Старт


1. Создать 
```shell
docker-compose up --build -d
```
2) Запустить контейнер
docker-compose up

3) Создать миграции
docker exec -it api aerich init-db

4) Создать суперюзера
docker exec -it api python scripts/createsuperuser.py

5) Если не выполняет команды
Войти в контейнер - docker exec -it api bash
Выполнить команды без docker exec -it api

6) Если нужно очистить БД
docker-compose down -v

7) Создать миграции
docker exec -it api aerich init-db
8) Выполнить миграции
docker exec -it api aerich init-db
