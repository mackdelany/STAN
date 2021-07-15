from werkzeug.debug import DebuggedApplication

from stan.api import app

if __name__ == "__main__":

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    app.run()