# cs373-idb
NBA Stats SWE project

Github page: https://github.com/jmslocum16/cs373-idb

To run this project as is, you must have postgres running on some machine (and modify the link to it in Models.py) to point to it. There must exist two databases with the same set of tables: nba_stats, nba_player, nba_team, and nba_season. Then, on the machine you wish to run it, clone the repo to some known directory. Then, configure apache2 with the mod_wsgi module installed to point to serve.wsgi as the WSGI script alias for '/'.

python3 Dependencies:
flask
 -Werkzeug
 -Jinja2
 -itsdangerous
 -markupsafe
sqlalchemy
psycopg2

Database:
postgres

Serving dependencies:
apache2
mod_wsgi
