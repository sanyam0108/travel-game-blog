import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # This tells Flask to look for a file called index.html in a 'templates' folder
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 8080)))
