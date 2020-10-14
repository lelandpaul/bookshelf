from flask import send_from_directory, jsonify, render_template
from app import app
from app.years import Years
from app.models import Book, Reading


@app.route('/')
def index():
    books = sorted([b.book_dict() for b in Book.query.all()],
                   key=lambda x: x['id'])
    return render_template('shelves.html',
                           books=books)


@app.route("/<path:path>")
def svelte_client(path):
    return send_from_directory('../svelte/public/', path)


@app.route('/test_book')
def test_book():
    book = {
                'title': 'Title',
                'authors': [{'surname': 'Surname', 'other_names': 'Other Names'},
                            {'surname': '2', 'other_names': 'Author'}],
                'series': 'Series',
                'genres': ['sf', 'h'],
                'readings': [
                            {'year': '3G',
                             'date': '2020-01-05',
                             'rating': 3,
                             'reread': False,
                             'manner': 'aloud'
                             },
                            {' year': '4B',
                             'date': '2020-05-05',
                             'rating': 1,
                             'reread': True,
                             'manner': 'audio'
                             },
                    ]
            }
    return jsonify(book)


@app.route('/shelves')
def get_shelves():

    shelves = [
        {'label': year,
         'books':
         [r.book.id
          for r in sorted(
              Reading.query.all(),
              key=lambda x: x.date, reverse=True) if r.year == year]}
        for year in Years.year_names()]

    return jsonify(shelves)
