from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauthlib.client import OAuth

from database import DB
from seatgeek import SeatGeek
from ticketmaster import TicketMaster

app = Flask(__name__)
app.secret_key = 'your_secret_key'

oauth = OAuth(app)

github = oauth.remote_app(
    'github',

    consumer_key='26beb9c55f16eacb1b5c',
    consumer_secret='db8b120222cb55f9010a692f4570d23a583d3256',


    request_token_params=None,
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

ticketMaster = TicketMaster()


@app.route('/')
def index():
    if 'github_token' in session:
        return redirect(url_for('query_page'))
    return 'Hello, this is the home page! <a href="/login">Login with GitHub</a>'


@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('index'))


@app.route('/callback')
def authorized():
    response = github.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['github_token'] = (response['access_token'], '')
    user_info = github.get('user')
    return redirect(url_for('query_page', user_info=user_info))


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


db = DB()
seatgeek = SeatGeek()


# HAOHAOHAO
@app.route('/query', methods=['GET', 'POST'])
def query_page():
    user_info = None
    if 'github_token' in session:
        user_info = github.get('user')

    matches = None
    if request.method == 'POST':

        start_date = request.form.get('start_date')
        print(f"query date {start_date}")

        matches = db.fetch(start_date)

        if len(matches) != 0:
            print("db is not empty")

        else:

            print("query db is empty, query from the website")
            seatResult = seatgeek.match_date(start_date)
            print(f"seatResult {seatResult}")
            matches = ticketMaster.match_date(start_date)
            matches.extend(seatResult)

            db.save(start_date, matches)

    return render_template('query.html', user_info=user_info, matches=matches)


if __name__ == '__main__':
    app.run(debug=True)

# https://github.com/settings/applications/
