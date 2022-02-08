import csv
import os

from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

# Путь папки с импортируемыми файлами
DATA_DIR = os.path.join(BASE_DIR, 'static', 'data')


class Command(BaseCommand):
    help = 'Импорт данных из csv-файла в БД'

    def add_arguments(self, parser):
        """Список аргументов."""

        # Пользователи
        parser.add_argument(
            '-users',
            action='store_true',
            default=False,
            help='Импорт данных из users.csv в БД User'
        )

        # Категории (типы) произведений
        parser.add_argument(
            '-category',
            action='store_true',
            default=False,
            help='Импорт данных из category.csv в БД Category'
        )

        # Категории жанров
        parser.add_argument(
            '-genre',
            action='store_true',
            default=False,
            help='Импорт данных из genre.csv в БД Genre'
        )

        # Произведения, к которым пишут отзывы
        parser.add_argument(
            '-titles',
            action='store_true',
            default=False,
            help='Импорт данных из titles.csv в БД Title'
        )

        # Связь между произведениями и их жанрами
        parser.add_argument(
            '-genre_title',
            action='store_true',
            default=False,
            help='Импорт данных из genre_title.csv в БД GenreTitle'
        )

        # Отзывы
        parser.add_argument(
            '-review',
            action='store_true',
            default=False,
            help='Импорт данных из review.csv в БД Review'
        )

        # Коментарии к отзывам
        parser.add_argument(
            '-comments',
            action='store_true',
            default=False,
            help='Импорт данных из comments.csv в БД Comment'
        )

    def user_handle(self, file):
        with open(file, mode='r', encoding="utf-8") as cvs_file:
            dr = csv.DictReader(cvs_file)
            for row in dr:
                User.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )

    def category_handle(self, file):
        with open(file, mode='r', encoding="utf-8") as cvs_file:
            dr = csv.DictReader(cvs_file)
            for row in dr:
                Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

    def genre_handle(self, file):
        with open(file, mode='r', encoding="utf-8") as cvs_file:
            dr = csv.DictReader(cvs_file)
            for row in dr:
                Genre.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

    def titles_handle(self, file):
        with open(file, mode='r', encoding="utf-8") as cvs_file:
            dr = csv.DictReader(cvs_file)
            for row in dr:
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category'],
                )

    def genre_title_handle(self, file):
        with open(file, mode='r', encoding="utf-8") as cvs_file:
            dr = csv.DictReader(cvs_file)
            for row in dr:
                GenreTitle.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id'],
                )

    def review_handle(self, file):
        with open(file, mode='r', encoding="utf-8") as cvs_file:
            dr = csv.DictReader(cvs_file)
            for row in dr:
                Review.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                )

    def comments_handle(self, file):
        with open(file, mode='r', encoding="utf-8") as cvs_file:
            dr = csv.DictReader(cvs_file)
            for row in dr:
                Comment.objects.create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date'],
                )

    def handle(self, *args, **options):
        """Список действий для каждого аргумента."""

        # Пользователи
        if options['users']:
            self.user_handle(os.path.join(DATA_DIR, 'users.csv'))

        # Категории (типы) произведений
        if options['category']:
            self.category_handle(os.path.join(DATA_DIR, 'category.csv'))

        # Категории жанров
        if options['genre']:
            self.genre_handle(os.path.join(DATA_DIR, 'genre.csv'))

        # Произведения, к которым пишут отзывы
        if options['titles']:
            self.titles_handle(os.path.join(DATA_DIR, 'titles.csv'))

        # Связь между произведениями и их жанрами
        if options['genre_title']:
            self.genre_title_handle(os.path.join(DATA_DIR, 'genre_title.csv'))

        # Отзывы
        if options['review']:
            self.review_handle(os.path.join(DATA_DIR, 'review.csv'))

        # Коментарии к отзывам
        if options['comments']:
            self.comments_handle(os.path.join(DATA_DIR, 'comments.csv'))
