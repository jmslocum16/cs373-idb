import os.path

from flask import Flask
app = Flask(__name__, static_url_path='static_html')


@app.route('/')
def splash():
    return send_from_directory('/', filename="splash.html")

@app.route('/player/<player_id>')
def get_player_page(player_id):
    if os.path.isfile('/static_html/players/' + player_id):
        return send_from_directory('/players/', filename=player_id)
    #send_from_directory('/', filename='404.html')

@app.route('/season/<season_id>')
def get_season_page(season_id):
    if os.path.isfile('/static_html/seasons/' + season_id):
        return send_from_directory('/seasons/', filename=season_id)
    #send_from_directory('/', filename='404.html')

@app.route('/team/<team_id>')
def get_season_page(team_id):
    if os.path.isfile('/static_html/teams/' + team_id):
        return send_from_directory('/teams/', filename=team_id)
    #send_from_directory('/', filename='404.html')


if __name__ == "__main__":
    app.run()
