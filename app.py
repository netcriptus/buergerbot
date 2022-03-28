from web_app import create_app, socketio

app = create_app()

def run_app(*args):
    socketio.run(app, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    socketio.run(app)
