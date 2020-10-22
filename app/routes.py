from flask import send_from_directory, jsonify, render_template, request
from app import app
from app.years import Years
from app.models import Book, Reading, Series

# Serve Svelte apps
@app.route("/<path:path>")
def svelte_client(path):
    return send_from_directory('../svelte/public/', path)



# Serve the main page
@app.route('/')
def index():
    books = sorted([b.book_dict() for b in Book.query.all()],
                   key=lambda x: x['id'])
    return render_template('shelves.html',
                           books=books)





categories = {
    'year': Years.year_names(),
    'rating': range(1, 4)[::-1],
}

sources = {
    'reading': Reading.query,
    'book': Book.query,
}

# Serve filtered shelves
@app.route('/shelves')
def get_shelves():

    categorize_by = request.args.get('categorize_by')
    cats = categories[categorize_by]
    source = sources[request.args.get('source')]
    sort_by = request.args.get('sort_by')

    shelves = [
        {'label': cat,
         'books':
            [x.book.id
             for x in sorted(
                    source.all(),
                    key=lambda x: getattr(x, sort_by)
                )
                 if getattr(x, categorize_by) == cat]
             }
        for cat in cats
    ]

    return jsonify(shelves)

@app.route('/series')
def get_series():
    series_title = request.args['title']
    series = Series.query.filter_by(name=series_title).first()
    if series is None:
        return jsonify([{'order': 'not found',
                        'book': 'not found',
                        'book_id': 'not found'}])
    books_in_series = [ {
        'order': book.series_order,
        'book': book.title,
        'book_id': book.id
        }
        for book in series.books
    ]
    return jsonify(books_in_series)
