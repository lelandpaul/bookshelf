from app import db
from app.years import Years
from statistics import mean


class Author(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    surname = db.Column('surname', db.String(128), index=True)
    other_names = db.Column('other_names', db.String(128))
    white_author = db.Column('white_author', db.Boolean)
    gender = db.Column('author_gender', db.String(32))
    books = db.relationship("BookAuthorAssociation", back_populates="author")

    def __repr__(self):
        return '<Author {}>'.format(self.surname)


class BookAuthorAssociation(db.Model):
    author_id = db.Column(
        'author_id_fk',
        db.Integer,
        db.ForeignKey('author.id'),
        primary_key=True)
    tower_id = db.Column(
        'book_id_fk',
        db.Integer,
        db.ForeignKey('book.id'),
        primary_key=True)
    author = db.relationship('Author', back_populates='books')
    book = db.relationship('Book', back_populates='author')

    def __repr__(self):
        return '<BookAuthor {} -- {}>'.format(
            self.book.title, self.author.surname)


class Series(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(128), index=True)
    books = db.relationship('Book', back_populates='series_rel')

    def __repr__(self):
        return '<Series {}>'.format(self.name)


class Book(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title = db.Column('title', db.String(128), index=True)
    author = db.relationship('BookAuthorAssociation', back_populates="book")

    genre = db.Column('genre', db.String(128))

    @property
    def genres(self):
        return self.genre.split(',')

    @staticmethod
    def all_genres():
        return set(genre for book in Book.query.all()
                   for genre in book.genres if genre)

    award = db.Column('awards', db.String(128))

    @property
    def awards(self):
        return self.award.split(',')


    series_id = db.Column(
        'series_id_fk',
        db.Integer,
        db.ForeignKey('series.id'))
    series_rel = db.relationship('Series', back_populates='books')
    series_order = db.Column('series_order', db.Integer, nullable=True)

    readings = db.relationship('Reading', back_populates='book')

    @property
    def average_rating(self):
        return mean([r.rating for r in self.readings])

    recommender = db.Column('recommender', db.String(128))

    @property
    def max_rating(self):
        if len(self.readings) == 0:
            return 1
        return max([r.rating for r in self.readings])

    @property
    def last_read(self):
        try:
            return max([r.date for r in self.readings])
        except ValueError:
            return None

    @property
    def date(self):
        return self.last_read

    @property
    def year(self):
        if self.last_read is None:
            return 'Unread'
        return Years.get(self.last_read)

    def __repr__(self):
        return '<Book {}>'.format(self.title)

    def book_dict(self):

        author_dicts = [{'surname': a.author.surname,
                         'other_names': a.author.other_names,
                         'white': a.author.white_author,
                         'gender': a.author.gender}
                        for a in self.author]

        reading_dicts = [{'year': r.year,
                          'date': str(r.date),
                          'rating': r.rating,
                          'reread': r.reread,
                          'manner': r.manner}
                         for r in self.readings]

        book_dict = {
            'id': self.id,
            'title': self.title,
            'genres': self.genres,
            'awards': self.awards,
            'series': self.series_rel.name if self.series_rel else None,
            'series_order': self.series_order,
            'recommender': self.recommender,
            'authors': author_dicts,
            'readings': reading_dicts }

        full_text = '^'.join([key + ':' + str(val) for key, val in
                              book_dict.items()])
        book_dict['full_text'] = full_text.lower()

        return book_dict


class Reading(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)

    book_id = db.Column('book_id_fk', db.Integer, db.ForeignKey('book.id'))
    book = db.relationship('Book', back_populates='readings')

    date = db.Column('date', db.Date, nullable=True)

    rating = db.Column('rating', db.Integer)

    reread = db.Column('reread', db.Boolean, default=False)
    manner = db.Column('manner', db.String(32), default='print')

    def __repr__(self):
        return '<Reading {} -- {}>'.format(self.book.title, self.year)

    @property
    def year(self):
        return Years.get(self.date)

    @property
    def book_title(self):
        return self.book.title
