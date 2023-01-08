import logging
from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

files_to_download = {
    User: 'static/data/users.csv',
    Category: 'static/data/category.csv',
    Genre: 'static/data/genre.csv',
    Title: 'static/data/titles.csv',
    Review: 'static/data/review.csv',
    Comment: 'static/data/comments.csv',
    'Genre_Title': 'static/data/genre_title.csv',
}

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = 'Load data in models from .csv file.'

    def handle(self, *args, **options):
        for model, file in files_to_download.items():
            logging.info(
                f'Load data from file {file} in model {model}...')

            for row in DictReader(open(f'./{file}', encoding='cp1251')):
                if model == 'Genre_Title':
                    genre = Genre.objects.get(pk=row['genre_id'])
                    title = Title.objects.get(pk=row['title_id'])
                    title.genre.add(genre)
                else:
                    obj = model(**row)
                    obj.save()

        logging.info('Load data complete!')
