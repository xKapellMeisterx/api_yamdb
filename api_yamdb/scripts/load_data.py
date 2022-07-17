import csv
import io

from reviews.models import Category, Comment, Genre, Review, Title, User
from django.db.utils import IntegrityError


def get_fields(row):
    if row.get('author'):
        row['author'] = User.objects.get(pk=row['author'])
    if row.get('review_id'):
        row['review'] = Review.objects.get(pk=row['review_id'])
    if row.get('title_id'):
        row['title'] = Title.objects.get(pk=row['title_id'])
    if row.get('category'):
        row['category'] = Category.objects.get(pk=row['category'])
    if row.get('genre'):
        row['genre'] = Genre.objects.get(pk=row['genre'])
    return row


def run():
    # set this value to True, in case you need
    # to clean db before injecting data:
    ERASE_ALL = False

    DIC = {
        User: 'static/data/users.csv',
        Category: 'static/data/category.csv',
        Genre: 'static/data/genre.csv',
        Title: 'static/data/titles.csv',
        Review: 'static/data/review.csv',
        Comment: 'static/data/comments.csv',
        'title_genre': 'static/data/genre_title.csv',
    }

    for key in DIC:
        if ERASE_ALL:
            key.objects.all().delete()
            print(
                f'All existing records for table {key.__name__} were erased.'
            )

        with io.open((DIC[key]), encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            data = []
            for row in reader:
                try:
                    temp_row = dict(zip(header, row))
                    row_fixed = get_fields(temp_row)
                    data.append(row_fixed)
                except Exception as e:
                    print(f'Failed with error: {e}')

            successful = 0
            failed = 0
            for row in data:
                try:
                    _, s = key.objects.get_or_create(**row)
                    if s:
                        successful += 1
                except IntegrityError as e:
                    print(f'Failed with error: {e}')
                    failed += 1

            print(
                f'Successfully created ojects type {key.__name__}:'
                f'{successful}, failed: {failed}.'
            )

    with io.open(DIC.get('title_genre'), encoding='utf-8') as file:
        reader = csv.reader(file)
        genres_dict = {}
        for row in reader:
            try:
                title = Title.objects.get(id=row[1])
                if title in genres_dict:
                    genres_dict[title].append(Genre.objects.get(id=row[2]))
                else:
                    genres_dict[title] = [Genre.objects.get(id=row[2])]
            except KeyError as k:
                print(f'Genres title key error: {k}')

        for key, value in genres_dict.items():
            try:
                key.genre.set(value)
                key.save()
            except Exception as e:
                print(f'Insertion error {e}')
