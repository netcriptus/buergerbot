#! /usr/bin/env python3

from flask import Flask, render_template
from flask_socketio import SocketIO
from apscheduler.schedulers.background import BackgroundScheduler
from buergerbot import fetch_months, extract_links, get_month_name, retry_time

app = Flask(__name__, template_folder=".", static_folder="static")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
time_left = None


def fetch_data():
    html_data = ''
    months = fetch_months()
    for month in months:
        html_data += f'<h2>{get_month_name(month)}</h2>'
        links = extract_links(month)
        html_data += '<ul>'
        if links:
            html_data += '\n'.join([f'<li><a target=”_blank” href={link[1]}>{link[0]}</a></li>' for link in links])
        html_data += '</ul>'
    return html_data

def update_calendar():
    global time_left
    html_data = None
    if not time_left:
        html_data = fetch_data()
        time_left = retry_time + 1
    time_left -= 1

    #job emits on websocket
    data = {'html_data': html_data, 'retry_time': f'Next update in {time_left}'}
    socketio.emit('calendar update', data, broadcast=True)

scheduler = BackgroundScheduler()
scheduler.add_job(update_calendar, 'interval', seconds=1, max_instances=1)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
