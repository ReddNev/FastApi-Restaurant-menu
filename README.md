# Старт


1. Создать 
```shell
docker-compose up --build -d
```
2) Запустить контейнер
docker-compose up

3) Создать миграции
docker exec -it useful-back aerich init-db

4) Создать суперюзера
docker exec -it useful-back python scripts/createsuperuser.py

5) Если не выполняет команды
Войти в контейнер - docker exec -it useful-back bash
Выполнить команды без docker exec -it useful-back

6) Если нужно очистить БД
docker-compose down -v

7) Создать миграции
docker exec -it useful-back aerich migrate

8) Выполнить миграции
docker exec -it useful-back aerich upgrade
