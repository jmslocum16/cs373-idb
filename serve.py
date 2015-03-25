import os.path

from flask import Flask
app = Flask(__name__, static_folder='static_html')
app.debug = False

STATIC_FOLDER = './static_html/' 


@app.route('/')
def root():
    return app.send_static_file('splash.html')

@app.route('/splash.html')
def splash():
    return app.send_static_file('splash.html')

@app.route('/about.html')
def about():
    return app.send_static_file('about.html')

@app.route('/sorttable.js')
def sorttable():
    return app.send_static_file('sorttable.js')

@app.route('/players/<player_id>')
def get_player_page(player_id):
    static_file = 'players/' + player_id
    if os.path.isfile(STATIC_FOLDER + static_file):
        return app.send_static_file(static_file)

@app.route('/seasons/<season_id>')
def get_season_page(season_id):
    static_file = 'seasons/' + season_id
    if os.path.isfile(STATIC_FOLDER + static_file):
        return app.send_static_file(static_file)

@app.route('/teams/<team_id>')
def get_team_page(team_id):
    static_file = 'teams/' + team_id
    if os.path.isfile(STATIC_FOLDER + static_file):
        return app.send_static_file(static_file)

if __name__ == "__main__":
    app.run('0.0.0.0')
