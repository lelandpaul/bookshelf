# coding: utf-8

from app import app, socketio, db


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            }


if __name__ == '__main__':
    socketio.run(app=app, host='0.0.0.0',port=8080)
