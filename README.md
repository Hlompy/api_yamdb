
# Яндекс.Практикум. Спринт 9

#### Название: Проект «API для Yatube»
#### Папка: api_yamdb
#### Группа: когорта 25
#### Когда: 2022 год

------------

# Описание:
Проект YaMDb собирает отзывы пользователей на произведения, которые делятся на категории: «Книги», «Фильмы», «Музыка». Категории, в дальнейшем, могут быть добавлены/отредактированы администратором. Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.


## Запуск проекта

Создайте и активируйте виртуальное окружение (для *nix/MacOS):

    python3 -m venv venv
    source venv/bin/activate

Создание и активация виртуального окружения длв Windows немного отличаеися:

    py -m venv venv
    venv\Scripts\activate

Установите зависимости из файла requirements.txt:

    pip install -r requirements.txt

Выполните миграции:

    python3 manage.py migrate


Запустите проект

    python3 manage.py runserver

## Лицензия
[MIT](https://ru.wikipedia.org/wiki/%D0%9B%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F_MIT)

