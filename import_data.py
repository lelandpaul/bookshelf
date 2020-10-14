from app.models import *
from csv import DictReader
from datetime import date

# Import Authors

print('Importing authors...')

with open('data_to_import/authors.csv', 'r', encoding='utf-8-sig') as infile:
    authors = DictReader(infile)

    for author in authors:
        a = Author(surname=author['Last Name'].strip(),
                   other_names=author['First Name'].strip(),
                   white_author=author['White?'] == 'checked',
                   gender=author['Gender'].lower().strip())
        db.session.add(a)
    db.session.commit()

print('...done.')

# Import Series

print('Importing series...')

with open('data_to_import/series.csv', 'r', encoding='utf-8-sig') as infile:
    series = DictReader(infile)

    for ser in series:
        s = Series(name=ser['Name'].strip())
        db.session.add(s)

    db.session.commit()

print('...done')


# Import Books

print('Importing books...')

with open('data_to_import/books.csv', 'r', encoding='utf-8-sig') as infile:
    books = DictReader(infile)

    for book in books:
        b = Book(title=book['Title'].strip(),
                 genre=book['Genres'].strip().lower(),
                 award=book['Awards'].strip(),
                 recommender=book['Recommender'].strip(),
                 series_rel=Series.query.filter_by(name=book['Series']).first())

        db.session.add(b)

        for author_name in book['Author'].split(','):
            a = Author.query.filter_by(surname=author_name).first()
            rel = BookAuthorAssociation(book=b, author=a)
            db.session.add(rel)

    db.session.commit()

print('...done')


# Import Readings

print('Importing readings...')

with open('data_to_import/readings.csv', 'r', encoding='utf-8-sig') as infile:
    readings = DictReader(infile)

    for reading in readings:
        bs_by_title = Book.query.filter_by(title=reading['Book'].strip(' "')).all()

        b = [b for b in bs_by_title if b.author[0].author.surname in reading['Author']][0]

        if b is None:
            print('Bad reading: ' + str(reading))

        r = Reading(book=b,
                    date=date.fromisoformat(reading['Date']),
                    rating=int(reading['Rating']),
                    reread=reading['Reread'] == 'checked')

        if reading['Audio'] == 'checked':
            r.manner = 'audio'
        elif reading['Read Aloud'] == 'checked':
            r.manner = 'aloud'

        db.session.add(r)

    db.session.commit()

print('...done')

