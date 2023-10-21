# yatube_project
Проект социальной сети
## Описание
Виртуальная площадка в которой пользователи могут создавать свои страницы, просматривать другие, подписываться на авторов, комментировать их записи, отправлять свои записи сообщества. 

Приятного ознакомления мой друг!
### Технологии
Python 3.9
Django 2.2.19
### Запуск проекта в dev-режиме
- Склонируйте проект себе на комьютер
```
git clone git@github.com:Artyom-Serov/yatube_project.git
``` 
- Установите в корневую папку и активируйте виртуальное окружение
```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```
- Обновите и установите pip
```
python3 -m pip install --upgrade pip
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Перейдите в директорию с файлом manage.py и выполните миграции:
```
cd yatube
```
```
python manage.py makemigrations
```
```
python manage.py migrate
```
- Запустите проект:
```
python manage.py runserver 127.0.0.1:8080
```
### Авторы
Артём Серов, кагорта 61 Яндекс.Практикум
