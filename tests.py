import unittest
from storage.genre import Genre
from storage.author import Author
from storage.book import Book
from server import app
from wiring import Wiring
import json
import bson


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.wiring = Wiring()

    def tearDown(self):
        db_name = app.config['MONGO_DATABASE']
        self.wiring.mongo_client.drop_database(db_name)

    def test_empty_genres(self):
        rv = self.app.get('/api/v1/genres')
        assert rv.status_code == 404

    def test_genres(self):
        genre = Genre(slug='fb_genre', name='Новый жанр')
        self.wiring.genre_dao.create(genre)
        rv = self.app.get('/api/v1/genres')
        assert b'fb_genre' in rv.data

    def test_empty_authors(self):
        rv = self.app.get('/api/v1/authors/1')
        assert rv.status_code == 400

    def test_author(self):
        author = Author(last_name='Иванов', first_name='Пётр', middle_name='Степанович')
        self.wiring.author_dao.create(author)
        rv = self.app.get('/api/v1/authors/{}'.format(author.id))
        assert rv.status_code == 200

    def test_search_by_lastname(self):
        author_one = Author(last_name='Пушкин', first_name='Александр', middle_name='Сергеевич')
        author_two = Author(last_name='Пушкин', first_name='Пётр', middle_name='Алексеевич')
        author_three = Author(last_name='Лермонтов', first_name='Михаил', middle_name='Юрьевич')
        self.wiring.author_dao.create(author_one)
        self.wiring.author_dao.create(author_two)
        self.wiring.author_dao.create(author_three)

        rv = self.app.get('/api/v1/authors/by_name/Пушкин')
        data = json.loads(rv.data)
        assert len(data) == 2

    def test_find_author(self):
        author_one = Author(last_name='Высоцкий', first_name='Александр', middle_name='Сергеевич')
        author_two = Author(last_name='Высоцкий', first_name='Пётр', middle_name='Алексеевич')
        self.wiring.author_dao.create(author_one)
        self.wiring.author_dao.create(author_two)

        rv = self.app.get('/api/v1/authors/by_full_name/Высоцкий/Оксана/Александровна')
        assert rv.status_code == 404

        rv = self.app.get('/api/v1/authors/by_full_name/Высоцкий/Александр/Сергеевич')
        data = json.loads(rv.data)
        assert data['last_name'] == 'Высоцкий'
        assert data['first_name'] == 'Александр'
        assert data['middle_name'] == 'Сергеевич'

    def test_find_first_letters(self):
        author_one = Author(last_name='Петров', first_name='Александр', middle_name='Сергеевич')
        author_two = Author(last_name='Петрова', first_name='Пётр', middle_name='Алексеевич')
        author_three = Author(last_name='Петренко', first_name='Михаил', middle_name='Юрьевич')
        self.wiring.author_dao.create(author_one)
        self.wiring.author_dao.create(author_two)
        self.wiring.author_dao.create(author_three)

        rv = self.app.get('/api/v1/authors/start_with/Петр')
        data = json.loads(rv.data)
        assert len(data) == 3
        assert 'Петр' in data[0]['last_name']
        assert 'Петр' in data[1]['last_name']
        assert 'Петр' in data[2]['last_name']

    def test_book(self):
        author_one = Author(last_name='Иванов', first_name='Иван', middle_name='Сергеевич')
        genre_one = Genre(slug='fb_genre_one', name='Жанр 1')
        book = Book(
            name='Тестовая книга',
            authors=[bson.ObjectId(author_one.id)],
            filename='1287831',
            added='2019-01-01',
            genres=['fb_genre_one'],
            lang='ru',
            deleted='0',
            sernum=1,
            series='Серия',
            keywords=['Фантастика', 'Новое']
        )
        self.wiring.book_dao.create(book)
        rv = self.app.get('/api/v1/books/{}'.format(book.id))
        assert rv.status_code == 200

    def test_book_by_author(self):
        author_one = Author(last_name='Володин', first_name='Александр', middle_name='Сергеевич')
        author_two = Author(last_name='Перов', first_name='Пётр', middle_name='Алексеевич')
        author_three = Author(last_name='Перумов', first_name='Михаил', middle_name='Юрьевич')
        self.wiring.author_dao.create(author_one)
        self.wiring.author_dao.create(author_two)
        self.wiring.author_dao.create(author_three)

        book_one = Book(name='Книга 1', authors=[bson.ObjectId(author_one.id)], filename='000001', added='2019-01-01',
            genres=['fb_genre_one'], lang='ru', deleted='0', sernum=1, series='Серия', keywords=['Фантастика', 'Новое'])
        book_two = Book(name='Книга 2', authors=[bson.ObjectId(author_one.id)], filename='000001', added='2019-01-01',
            genres=['fb_genre_one'], lang='ru', deleted='0', sernum=1, series='Серия', keywords=['Фантастика', 'Новое'])
        book_three = Book(name='Книга 3',authors=[bson.ObjectId(author_two.id)], filename='000001',added='2019-01-01',
            genres=['fb_genre_one'], lang='ru', deleted='0', sernum=1, series='Серия', keywords=['Фантастика', 'Новое'])

        self.wiring.book_dao.create(book_one)
        self.wiring.book_dao.create(book_two)
        self.wiring.book_dao.create(book_three)

        rv = self.app.get('/api/v1/books/by_author/{}'.format(author_one.id))
        assert rv.status_code == 200

        data = json.loads(rv.data)
        assert len(data) == 2


if __name__ == '__main__':
    unittest.main()
