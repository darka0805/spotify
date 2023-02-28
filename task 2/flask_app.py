from flask import Flask, render_template, request
from map_main import main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/map', methods=['POST'])
def show_map():
    if request.method == 'POST':
        artist = request.form['artist']
        main(artist)
        return render_template('Map.html')

if __name__ == '__main__':
    app.run(debug=True)