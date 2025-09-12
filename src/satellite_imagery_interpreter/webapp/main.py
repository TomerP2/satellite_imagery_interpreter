from flask import Flask
from webapp.routes import init_routes
import webbrowser
from threading import Timer

app = Flask(__name__)

# Initialize routes
init_routes(app)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True)
