from flask_socketio import emit
from flask import session, request
from app import socketio, app
from app.models import *
from app.years import Years

@socketio.on('c_request_shelves')
def on_request_shelves(json):
    print('shelves requested')


    shelves = [ { 'label': year,
                  'books': [ r.book.id for r in sorted(Reading.query.all(),
                                            key=lambda x: x.date,
                                            reverse=True) if r.year == year ] \
                 }
                for year in Years.year_names() ]

    print(shelves)

    emit('s_set_shelves', {'shelves': shelves})





"""

general form for shelving:
[ { category, shelf } for category in categories }

Each shelf is either going to be of Readings (i.e. books can appear multiple times)
or of Books (books can appear only once)

Some things one might want to order by: (all keys available from Book)
- Average rating
- Individual rating
- Author surname
- Title
- Number of readings
- Reading date
- Series order (dependent on series)

Some things one might want to categorize by:
- Author (book appear at most once per shelf) (categories from Author)
- Genre (books appear at most once per shelf) (categories from Book)
- Series (books appear at most once)          (categories from Series)
- Manner (books appear multiple times)        (categories from Reading)
- Year (books appear multiple times)          (categories from Year)
- Rating (books appear multiple times)        (categories from Reading)



"""

# shelves [ { 'label': category,
#             'books': [ book.id for book in
