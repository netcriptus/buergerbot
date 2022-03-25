#! /usr/bin/env python3

from web_app import socketio
from apscheduler.schedulers.background import BackgroundScheduler
from web_app.buergerbot import fetch_months, extract_links, get_month_name, retry_time

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
    socketio.emit('fetching update', {}, broadcast=True)

    html_data = None
    html_data = fetch_data()
    data = {'html_data': html_data, 'next_refresh': retry_time}

    socketio.emit('calendar update', data, broadcast=True)

@socketio.on('connected')
def schedule_task(_):
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_calendar, 'interval', seconds=retry_time)
    scheduler.start()
    update_calendar()
